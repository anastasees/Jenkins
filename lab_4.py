from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# ------------------- СЕРВІС ДЛЯ ЛІЧИЛЬНИКІВ -------------------
class MeterService:
    def __init__(self):
        # словник: {meter_id (str): status (str)}
        self.meters = {}

    def add_meter(self, meter_id, status="Не повірений"):
        # Перетворюємо id у рядок — у вебі зазвичай id надходить як рядок
        meter_id = str(meter_id)
        # Перевірка на "хешованість" не потрібна для рядків, але лишимо перевірку типів
        try:
            hash(meter_id)
        except TypeError:
            raise ValueError("ID лічильника має бути хешованого типу")
        # Уникаємо дублювання однакових id
        if meter_id in self.meters:
            return f"Лічильник з ID {meter_id} вже існує"
        self.meters[meter_id] = status
        return f"Додано: {meter_id} -> {status}"

    def remove_meter(self, meter_id):
        meter_id = str(meter_id)
        if meter_id in self.meters:
            status = self.meters.pop(meter_id)
            return f"Видалено: {meter_id} -> {status}"
        return f"Лічильник з ID {meter_id} не знайдено"

    def update_status(self, meter_id, status):
        meter_id = str(meter_id)
        if meter_id in self.meters:
            self.meters[meter_id] = status
            return f"Оновлено: {meter_id} -> {status}"
        return f"Лічильник з ID {meter_id} не знайдено"

    def check_meter(self, meter_id):
        return self.meters.get(str(meter_id))

    def display_all(self):
        # повертаємо копію, щоб зовнішній код не змінював внутрішній словник
        return self.meters.copy()

    def search_by_status(self, status):
        # точний пошук по статусу (чутливий до регістру)
        return [mid for mid, st in self.meters.items() if st == status]

    def search(self, keyword):
        # пошук по id або по включенню в id чи в статус (регістро-незалежно для зручності)
        kw = str(keyword).lower()
        results = []
        for mid, st in self.meters.items():
            if kw == mid.lower() or kw in mid.lower() or kw in st.lower():
                results.append((mid, st))
        return results


meter_service = MeterService()

# ------------------- УТИЛІТИ ДЛЯ ВІДОБРАЖЕННЯ -------------------
def show_meters_html():
    items = meter_service.display_all()
    if not items:
        return "<p>Список лічильників порожній</p>"
    html = "<table border='1' cellpadding='6' style='border-collapse:collapse; background:white;'>"
    html += "<tr><th>ID</th><th>Статус</th><th>Дії</th></tr>"
    for mid, st in items.items():
        html += (
            f"<tr><td>{mid}</td>"
            f"<td>{st}</td>"
            f"<td>"
            f"<a href='/delete/{mid}'>Видалити</a> | "
            f"<a href='/update/{mid}'>Змінити статус</a>"
            f"</td></tr>"
        )
    html += "</table>"
    return html

def search_results_html(results, keyword):
    if not results:
        return f"<p>Нічого не знайдено за '{keyword}'.</p>"
    html = f"<h3>Результати пошуку за '{keyword}':</h3><ul>"
    for mid, st in results:
        html += f"<li>ID: {mid} — Статус: {st} | <a href='/update/{mid}'>Змінити</a> | <a href='/delete/{mid}'>Видалити</a></li>"
    html += "</ul>"
    html += "<p><a href='/'>⬅ Повернутись</a></p>"
    return html

# ------------------- ВЕБ-РОУТИ -------------------
@app.route("/")
def home():
    html = """
    <html>
    <head>
        <title>Облік лічильників</title>
        <style>
            body { font-family: Arial; margin: 40px; background-color: #f2f6f9; }
            h1 { color: #222; }
            form { background: white; padding: 15px; margin-top: 20px; border-radius: 10px; width: fit-content; }
            input, select, button { margin: 6px; padding: 8px; }
            .summary { margin-top: 10px; padding: 10px; background: white; border-radius: 8px; width: fit-content; }
        </style>
    </head>
    <body>
        <h1> Облік лічильників</h1>
    """
    html += show_meters_html()
    html += f"<div class='summary'><b>Загальна кількість лічильників: {len(meter_service.display_all())}</b></div>"

    html += """
        <h3> Додати лічильник</h3>
        <form action="/add" method="post">
            Номер лічильника: <input name="meter_id" required>
            Статус:
            <select name="status">
                <option value="Не повірений" selected>Не повірений</option>
                <option value="Повірений">Повірений</option>
                <option value="Пошкоджений">Пошкоджений</option>
            </select>
            <button type="submit">Додати</button>
        </form>

        <h3> Пошук лічильника</h3>
        <form action="/search" method="get">
            Ключове слово або ID: <input name="keyword" required>
            <button type="submit">Шукати</button>
        </form>
    </body></html>
    """
    return html

@app.route("/add", methods=["POST"])
def add():
    meter_id = request.form.get("meter_id", "").strip()
    status = request.form.get("status", "Не повірений").strip()
    if not meter_id:
        # простий захист від пустого id
        return redirect(url_for("home"))
    meter_service.add_meter(meter_id, status)
    return redirect(url_for("home"))

@app.route("/delete/<meter_id>")
def delete(meter_id):
    meter_service.remove_meter(meter_id)
    return redirect(url_for("home"))

@app.route("/update/<meter_id>")
def update(meter_id):
    current = meter_service.check_meter(meter_id)
    if current is None:
        return redirect(url_for("home"))
    html = f"""
    <html><head><title>Оновити статус</title>
    <style>body {{ font-family: Arial; margin:40px; }}</style>
    </head><body>
    <h2>Оновити статус лічильника {meter_id}</h2>
    <form action="/update_status" method="post">
        <input type="hidden" name="meter_id" value="{meter_id}">
        Новий статус: <select name="new_status">
            <option value="Не повірений">Не повірений</option>
            <option value="Повірений">Повірений</option>
            <option value="Пошкоджений">Пошкоджений</option>
        </select>
        <button type="submit">Зберегти</button>
    </form>
    <p><a href="/">⬅ Повернутись</a></p>
    </body></html>
    """
    return html

@app.route("/update_status", methods=["POST"])
def update_status():
    meter_id = request.form.get("meter_id", "").strip()
    new_status = request.form.get("new_status", "").strip()
    if meter_id and new_status:
        meter_service.update_status(meter_id, new_status)
    return redirect(url_for("home"))

@app.route("/search")
def search():
    keyword = request.args.get("keyword", "").strip()
    if not keyword:
        return redirect(url_for("home"))
    results = meter_service.search(keyword)
    return search_results_html(results, keyword)

# ------------------- ПОЧАТКОВІ ДАНІ ТА ЗАПУСК -------------------
if __name__ == "__main__":
    # Декілька початкових лічильників для демонстрації
    meter_service.add_meter("123", "Не повірений")
    meter_service.add_meter("456", "Повірений")
    meter_service.add_meter("789", "Повірений")

    app.run(host="0.0.0.0", port=8080)
