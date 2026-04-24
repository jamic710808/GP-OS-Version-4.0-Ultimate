## Context

毛利分析 V3.0 目前提供 14 個分析頁面，但缺乏主動預警功能。管理層需手動檢視報告才能發現異常，存在資訊落後問題。本設計新增「預警中心」頁面，實現毛利率異常的即時監控與通知。

**現有架構：**
- 純前端單一 HTML 檔案
- 資料由 `DEFAULT_DATA` 物件提供
- 14 個 Tab 頁面，透過懶載入渲染

**約束條件：**
- 維持單一 HTML 架構（不引入後端）
- 使用現有 Chart.js 技術棧
- 向後相容現有資料結構

## Goals / Non-Goals

**Goals:**
- 提供預警中心儀表板，一目了然所有異常狀態
- 支援多維度預警設定（產品、客戶、地區、渠道）
- 異常時高亮顯示，支援 Email 通知（需用戶設定 SMTP）
- 預警記錄本地儲存（localStorage）

**Non-Goals:**
- 即時股價串接（非財務預警範疇）
- 行動應用程式
- 多用戶協作功能

## Decisions

### Decision 1: 預警資料結構
```javascript
AlertRule {
  id: string,
  dimension: 'product' | 'customer' | 'region' | 'channel',
  targetId: string,
  minMargin: number,   // 下限，null = 不限制
  maxMargin: number,   // 上限，null = 不限制
  enabled: boolean
}

AlertRecord {
  id: string,
  ruleId: string,
  timestamp: Date,
  actualMargin: number,
  status: 'triggered' | 'acknowledged' | 'resolved'
}
```

**Rationale:** 參考現有 `DEFAULT_DATA` 的 9 個資料鍵結構，預警維度對應現有維度（products/customers/regions/channels）。

### Decision 2: 預警觸發時機
- 資料載入時自動檢查所有規則
- 使用者修改篩選條件後重新檢查
- 不使用定時輪詢（避免增加複雜度）

**Rationale:** 純前端架構下，資料變更來自使用者操作，事件驅動比輪詢更高效。

### Decision 3: 通知機制
```javascript
NotifyConfig {
  email: string,
  smtpServer: string,
  smtpPort: number,
  enabled: boolean
}
```

**Alternatives Considered:**
- Webhook（需後端，超出範圍）
- Browser Notification（限同源限制，用途有限）
- **選擇 Email**（最實用，但需用戶設定 SMTP）

### Decision 4: 歷史記錄儲存
使用 `localStorage` 儲存 AlertRecord 陣列，上限 1000 筆，自動清除舊記錄。

**Rationale:** 單一 HTML 架構下，本地儲存是最簡單的持久化方案。

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Email SMTP 設定繁瑣 | 提供設定精靈，儲存後重複使用 |
| localStorage 空間有限（~5MB） | 限制記錄數量，定期清理 |
| 無法跨裝置同步 | 在文件說明限制，必要時可匯出 JSON |

## Open Questions

1. 預警閾值是否需要支援百分比或絕對值？
2. 是否需要支援「連續 N 期異常」才觸發的進階規則？
