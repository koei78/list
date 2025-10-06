import csv
import io
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response

from .db import get_cursor


bp = Blueprint("main", __name__)


def register_routes(app):
    app.register_blueprint(bp)


@bp.route("/")
def index():
    return redirect(url_for("main.list_records"))


@bp.route("/records")
def list_records():
    # データ一覧は常に1データセットのみ表示（最古のactive）
    after = request.args.get("after", type=int)
    with get_cursor() as cur:
        if after:
            cur.execute(
                "SELECT * FROM datasets WHERE status='active' AND id>? ORDER BY id ASC LIMIT 1",
                (after,),
            )
        else:
            cur.execute(
                "SELECT * FROM datasets WHERE status='active' ORDER BY id ASC LIMIT 1"
            )
        ds = cur.fetchone()

        if not ds:
            flash("処理対象のデータがありません", "success")
            return render_template("list.html", dataset=None, calls=[])

        dataset = dict(ds)
        cur.execute(
            "SELECT * FROM calls WHERE dataset_id=? ORDER BY id ASC",
            (dataset["id"],),
        )
        calls = [dict(r) for r in cur.fetchall()]

    return render_template("list.html", dataset=dataset, calls=calls)


@bp.route("/prospects")
def list_prospects():
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT d.*, COUNT(c.id) AS call_count
            FROM datasets d
            LEFT JOIN calls c ON c.dataset_id = d.id
            WHERE d.status='prospect'
            GROUP BY d.id
            ORDER BY d.created_at DESC, d.id DESC
            """
        )
        datasets = [dict(r) for r in cur.fetchall()]
    return render_template("datasets.html", title="見込み一覧", datasets=datasets, show_actions=False)


# 手動1件追加は廃止（CSV取り込みのみで登録）


@bp.route("/upload", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        file = request.files.get("file")
        shop_name = request.form.get("shop_name", "").strip()
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()
        next_call_date = request.form.get("next_call_date", "").strip()
        next_call_time = request.form.get("next_call_time", "").strip()

        if not file or file.filename == "":
            flash("CSVファイルを選択してください", "error")
            return render_template("upload.html")
        if not shop_name or not address:
            flash("店舗名と住所は必須です", "error")
            return render_template("upload.html")

        try:
            stream = io.StringIO(file.stream.read().decode("utf-8-sig"))
            reader = csv.DictReader(stream)
            print("CSVヘッダー:", reader.fieldnames)
        except Exception as e:
            print("CSV読み込みエラー:", e)
            flash("CSVの読み込みに失敗しました", "error")
            return render_template("upload.html")

        rows = []
        for i, row in enumerate(reader, start=1):
            normalized = {
                k.strip(): (v.strip() if isinstance(v, str) else v)
                for k, v in row.items()
                if k is not None
            }

            # vos_log.csv に合わせた必須列チェック
            if not (normalized.get("担当者") and normalized.get("電話番号")):
                continue

            rows.append(
    (
        normalized.get("ステータス") or "未設定",   # ← Noneを避ける
        normalized.get("担当者") or "不明",
        normalized.get("通話方向") or "不明",
        normalized.get("電話番号") or "",
        normalized.get("メモ") or "",
        normalized.get("日時") or "",
    )
)


        if not rows:
            flash("取り込める行がありません（CSV列名を確認してください）", "error")
            return render_template("upload.html")

        with get_cursor() as cur:
            cur.execute(
                "INSERT INTO datasets (shop_name, address, csv_name, phone, next_call_date, next_call_time) VALUES (?, ?, ?, ?, ?, ?)",
                (shop_name, address, file.filename, phone, next_call_date, next_call_time),
            )
            dataset_id = cur.lastrowid

            cur.executemany(
                """
                INSERT INTO calls (dataset_id, start_user_type, callee, call_flow, caller_number, content, date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [(dataset_id, *r) for r in rows],
            )

        flash(f"{len(rows)}件を取り込みました", "success")
        return redirect(url_for("main.list_records"))

    return render_template("upload.html")


@bp.post("/dataset/<int:dataset_id>/prospect")
def mark_prospect(dataset_id: int):
    with get_cursor() as cur:
        cur.execute("UPDATE datasets SET status='prospect' WHERE id=?", (dataset_id,))
    flash("見込みへ移動しました", "success")
    # 次のデータセットへ
    return redirect(url_for("main.list_records", after=dataset_id))


@bp.route("/dataset/<int:dataset_id>/discard" , methods=["GET", "POST"])
def discard_dataset(dataset_id: int):
    with get_cursor() as cur:
        # データセットを消すと紐づくcallsもON DELETE CASCADEで削除
        cur.execute("DELETE FROM datasets WHERE id=?", (dataset_id,))
    flash("削除しました", "success")
    # フォームから next が渡されていればそのページへ戻す（例: /prospects）
    next_url = request.form.get("next")
    if next_url:
        return redirect(next_url)
    # 次のデータセットへ（従来の挙動）
    return redirect(url_for("main.list_records", after=dataset_id))


@bp.post("/dataset/<int:dataset_id>/update_next_call")
def update_next_call(dataset_id: int):
    next_call_date = (request.form.get("next_call_date") or "").strip()
    next_call_time = (request.form.get("next_call_time") or "").strip()
    with get_cursor() as cur:
        cur.execute(
            "UPDATE datasets SET next_call_date=?, next_call_time=? WHERE id=?",
            (next_call_date, next_call_time, dataset_id),
        )
    flash("次回コール予定を更新しました", "success")
    # stay on list view for current dataset
    return redirect(url_for("main.list_records"))

@bp.get("/review")
def review():
    after = request.args.get("after", type=int)
    with get_cursor() as cur:
        if after:
            cur.execute(
                "SELECT * FROM datasets WHERE status='active' AND id>? ORDER BY id ASC LIMIT 1",
                (after,),
            )
        else:
            cur.execute(
                "SELECT * FROM datasets WHERE status='active' ORDER BY id ASC LIMIT 1"
            )
        ds = cur.fetchone()

        if not ds:
            flash("処理対象のデータがありません", "success")
            return redirect(url_for("main.list_records"))

        dataset = dict(ds)
        cur.execute(
            "SELECT * FROM calls WHERE dataset_id=? ORDER BY id ASC",
            (dataset["id"],),
        )
        calls = [dict(r) for r in cur.fetchall()]

    return render_template("review.html", dataset=dataset, calls=calls)


@bp.get("/dataset/<int:dataset_id>/csv")
def dataset_csv(dataset_id: int):
    # データセットの内容をCSVとしてダウンロード
    with get_cursor() as cur:
        cur.execute("SELECT * FROM datasets WHERE id=?", (dataset_id,))
        ds = cur.fetchone()
        if not ds:
            flash("データが見つかりません", "error")
            return redirect(url_for("main.list_records"))
        cur.execute(
            """
            SELECT start_user_type, callee, call_flow, caller_number, content, created_at
            FROM calls WHERE dataset_id=? ORDER BY id ASC
            """,
            (dataset_id,),
        )
        rows = cur.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    # Include dataset info and separate timestamps for dataset and call history
    writer.writerow([
        "shop_name",
        "address",
        "next_call_date",
        "next_call_time",
        "dataset_created_at",
        "start_user_type",
        "callee",
        "call_flow",
        "caller_number",
        "content",
        "call_created_at",
    ])
    for r in rows:
        writer.writerow([
            ds["shop_name"],
            ds["address"],
            ds.get("next_call_date") or "",
            ds.get("next_call_time") or "",
            ds["created_at"],
            r["start_user_type"],
            r["callee"],
            r["call_flow"] or "",
            r["caller_number"],
            r["content"] or "",
            r["created_at"],
        ])

    from flask import Response
    filename = (ds["csv_name"] or f"dataset_{dataset_id}.csv").replace("\r", " ").replace("\n", " ")
    return Response(
        output.getvalue().encode("utf-8-sig"),
        mimetype="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )


@bp.get('/api/prospects/top')
def api_prospects_top():
    """Return the latest prospect dataset and its calls.
    - Default: JSON response { dataset: {...}, calls: [...] }
    - ?format=csv で CSV を返します (same columns as dataset_csv for single dataset)
    """
    out_format = request.args.get('format', 'json').lower()
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM datasets WHERE status='prospect' ORDER BY created_at DESC, id DESC LIMIT 1"
        )
        ds = cur.fetchone()
        if not ds:
            body = json.dumps({'error': 'no prospect datasets found'}, ensure_ascii=False)
            return Response(body.encode('utf-8'), status=404, mimetype='application/json; charset=utf-8')
        dataset = dict(ds)
        cur.execute(
            "SELECT * FROM calls WHERE dataset_id=? ORDER BY id ASC",
            (dataset['id'],),
        )
        calls = [dict(r) for r in cur.fetchall()]

    if out_format == 'csv':
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow([
            "shop_name",
            "address",
            "next_call_date",
            "next_call_time",
            "dataset_created_at",
            "start_user_type",
            "callee",
            "call_flow",
            "caller_number",
            "content",
            "call_date",
        ])
        for r in calls:
            writer.writerow([
                dataset.get('shop_name'),
                dataset.get('address'),
                dataset.get('next_call_date') or '',
                dataset.get('next_call_time') or '',
                dataset.get('created_at'),
                r.get('start_user_type'),
                r.get('callee'),
                r.get('call_flow') or '',
                r.get('caller_number'),
                r.get('content') or '',
                r.get('date') or r.get('created_at') or '',
            ])
        filename = (dataset.get('csv_name') or f"dataset_{dataset['id']}.csv").replace("\r", " ").replace("\n", " ")
        return Response(out.getvalue().encode('utf-8-sig'), mimetype='text/csv; charset=utf-8', headers={
            'Content-Disposition': f'attachment; filename={filename}'
        })

    # Default JSON (ensure utf-8 and preserve Japanese characters)
    body = json.dumps({'dataset': dataset, 'calls': calls}, ensure_ascii=False)
    return Response(body.encode('utf-8'), mimetype='application/json; charset=utf-8')


@bp.get('/api/prospects/top/address')
def api_prospects_top_address():
    """Return only the address of the latest prospect dataset as JSON: {"address": "..."} """
    with get_cursor() as cur:
        cur.execute(
            "SELECT id, shop_name, address FROM datasets WHERE status='prospect' ORDER BY created_at DESC, id DESC LIMIT 1"
        )
        row = cur.fetchone()
        if not row:
            body = json.dumps({'error': 'no prospect datasets found'}, ensure_ascii=False)
            return Response(body.encode('utf-8'), status=404, mimetype='application/json; charset=utf-8')
        dataset = dict(row)
        # Get first call's caller_number for phone (if exists)
        cur.execute("SELECT caller_number FROM calls WHERE dataset_id=? ORDER BY id ASC LIMIT 1", (dataset['id'],))
        call_row = cur.fetchone()
        phone = call_row['caller_number'] if call_row and 'caller_number' in call_row.keys() else ''
        body = json.dumps({
            'shop_name': dataset.get('shop_name'),
            'address': dataset.get('address'),
            'phone': phone,
            'next_call_date': dataset.get('next_call_date') or '',
            'next_call_time': dataset.get('next_call_time') or ''
        }, ensure_ascii=False)
        return Response(body.encode('utf-8'), mimetype='application/json; charset=utf-8')
