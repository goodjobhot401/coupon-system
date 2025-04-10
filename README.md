# 🎟️ coupon-system

 一個以 `FastAPI` 為核心的優惠券服務，結合 `MySQL` 與 `Redis`，在高併發環境下仍能確保優惠券庫存一致性。專案內建 `docker‑compose`，只需一行指令即可在任何支援 `Docker` 的機器上快速啟動。

## 🏗️ Built with


`FastAPI + SQLAlchemy`：使用非同步 Web Framework 與 ORM

`MySQL`：永久儲存使用者、優惠券、領取紀錄

`Redis`：避免同時領取導致的超賣問題

`Docker`：使用容器化技術快速啟動所有依賴環境，自動建立資料表並寫入範例資料


## 📒 Docs Tree

```text
.
├── src
│   ├── database         --- DDL & DML 初始化
│   ├── helpers          --- 公用工具，時間單位換算
│   ├── infra            --- DB sesion 管理
│   ├── models           --- ORM DB schema
│   ├── repositories     --- 資料庫操作
│   ├── routers          --- Fastapi 入口路由
│   ├── schemas          --- Req & Res 結構
│   ├── services         --- 商業邏輯操作
│   └── workers          --- 背景任務
│       └── main.py      --- 伺服器主入口
├── .env.template        --- 環境變數樣板
├── .gitignore           --- Git 忽略設定
├── docker-compose.yml   --- 容器化設定
├── dockerfile           --- Docker 映像建置指令
├── LICENSE              --- 專案授權資訊
├── postman.json         --- Postman 測試集合
├── README.md            --- 專案說明文件
└── requirements.txt     --- Python 套件依賴清單

```

## 🚀 Getting Started

**Clone the repo**

```
git clone https://github.com/goodjobhot401/coupon-system.git
cd coupon-system
```


**Initialize**

```
docker compose up --build
```


**Schema**
---
`account`
| attributes | datatype         | Nullable |
|------------|------------------|----------|
| id         | Integer (PK)     | NO       | 
| name       | String(50)       | NO       |
| created_at | TIMESTAMP        | NO       |
| updated_at | TIMESTAMP        | NO       |
<br>

`coupon`
| 欄位        | 型別             | Nullable | 
|------------|------------------|----------|
| id         | Integer (PK)     | NO       |
| title      | String(250)      | NO       |
| type       | String(50)       | NO       | 
| stock      | Integer          | NO       |
| expires_at | TIMESTAMP        | NO       | 
| created_at | TIMESTAMP        | NO       |
| updated_at | TIMESTAMP        | NO       | 
<br>

`coupon_record`
| 欄位        | 型別                    | Nullable |
|------------|-------------------------|----------|
| id         | Integer (PK)            | NO       | 
| coupon_id  | Integer (FK coupon.id)  | NO       | 
| account_id | Integer (FK account.id) | NO       | 
| claim_at   | TIMESTAMP               | NO       | 
| used_at    | TIMESTAMP               | YES      |
| updated_at | TIMESTAMP               | NO       |
<br>


## 𓇠 Seed Data & Postman
啟動容器後，系統將自動插入：
- **2** 筆 `account`
- **2** 筆 `coupon`
- **6** 筆 `coupon_record`

💡 可直接使用根目錄的 `postman.json` 匯入至 Postman，快速測試所有 API 功能。

