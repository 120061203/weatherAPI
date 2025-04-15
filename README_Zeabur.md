
# 🌤️ Weather API - FastAPI + Zeabur 部署版

這是一個使用 FastAPI 製作的天氣查詢 API，搭配 OpenWeatherMap，並部署到 Zeabur。

---

## 📁 專案結構

```
backend/
├── main.py              # FastAPI 主程式
├── .env                 # 儲存 API 金鑰 (部署用 Zeabur 的 Secrets 管理)
├── requirements.txt     # Python 套件列表
└── static/
    └── index.html       # 前端查詢畫面（可作為測試）
```

---

## 🚀 快速開始（本機開發）

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

打開瀏覽器輸入：http://127.0.0.1:8000

---

## ☁️ 部署到 Zeabur

### 1️⃣ 上傳 `backend/` 到 GitHub

```bash
cd backend
git init
git add .
git commit -m "🚀 Initial commit"
gh repo create weather-backend --public --source=. --remote=origin --push
```

### 2️⃣ 到 [Zeabur](https://zeabur.com)

- 新增專案 → 連接 GitHub → 選你的 repo
- Runtime 選 Python
- Port 設為 `8000`
- 加入環境變數：
  ```
  OPENWEATHER_API_KEY=你的金鑰
  ```

### 3️⃣ 設定啟動指令

```
uvicorn main:app --host 0.0.0.0 --port 8000
```

### ✅ 完成部署！

打開網址就可以看到：
```
https://your-project-name.zeabur.app/weather?city=Taipei
```

---

## 💡 API 使用方式

```http
GET /weather?city=Taipei
```

### 回傳 JSON：
```json
{
  "城市": "Taipei",
  "天氣": "晴天",
  "氣溫": 26.5,
  "體感溫度": 28.1,
  "濕度": 70
}
```

---

## 🧑‍💻 作者

陳松林（小松）｜Made with ❤️ using FastAPI + Zeabur
