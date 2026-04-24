## 1. 資料結構擴展

- [ ] 1.1 在 `DEFAULT_DATA` 新增 `AlertRule` 類型定義
- [ ] 1.2 在 `DEFAULT_DATA` 新增 `AlertRecord` 類型定義
- [ ] 1.3 在 `DEFAULT_DATA` 新增 `NotifyConfig` 類型定義
- [ ] 1.4 新增 `alertRules` 陣列（預設空陣列）
- [ ] 1.5 新增 `alertHistory` 陣列（預設空陣列）
- [ ] 1.6 新增 `notifyConfig` 物件（Email 設定）

## 2. 預警核心邏輯

- [ ] 2.1 實作 `checkMarginAlert(rule, actualMargin)` 函式
- [ ] 2.2 實作 `triggerAlert(rule, actualMargin)` 函式
- [ ] 2.3 實作 `saveAlertToHistory(record)` 函式（含 localStorage 寫入）
- [ ] 2.4 實作 `loadAlertHistory()` 函式（含 1000 筆限制檢查）
- [ ] 2.5 實作 `sendEmailNotification(config, record)` 函式

## 3. 預警規則 CRUD

- [ ] 3.1 實作 `addAlertRule(rule)` 函式
- [ ] 3.2 實作 `updateAlertRule(id, updates)` 函式
- [ ] 3.3 實作 `deleteAlertRule(id)` 函式
- [ ] 3.4 實作 `toggleAlertRule(id)` 函式
- [ ] 3.5 實作 `getAlertRulesByDimension(dimension)` 函式

## 4. Alert Dashboard 頁面

- [ ] 4.1 新增 `renderAlertDashboard()` 渲染函式
- [ ] 4.2 實作預警摘要卡片（總數、待處理、已處理）
- [ ] 4.3 實作異常清單表格（依維度顯示、狀態標籤、操作按鈕）
- [ ] 4.4 實作維度篩選下拉選單
- [ ] 4.5 實作預警規則設定面板（新增/編輯/刪除表單）
- [ ] 4.6 實作 Tab 標題紅點提示邏輯

## 5. Alert History 功能

- [ ] 5.1 實作歷史查詢 `queryAlertHistory(filters)` 函式
- [ ] 5.2 實作狀態更新 `updateAlertStatus(id, newStatus)` 函式
- [ ] 5.3 實作批量更新 `bulkUpdateStatus(ids, newStatus)` 函式
- [ ] 5.4 實作 CSV 匯出 `exportAlertHistoryToCSV()` 函式
- [ ] 5.5 實作預警趨勢圖（Chart.js 折線圖）

## 6. Tab 整合

- [ ] 6.1 在 `TABS` 陣列新增「預警中心」
- [ ] 6.2 更新 `renderPage()` 判斷邏輯
- [ ] 6.3 更新 `switchTab()` 高亮邏輯

## 7. 設定儲存

- [ ] 7.1 實作 `saveAlertConfig()` 儲存至 localStorage
- [ ] 7.2 實作 `loadAlertConfig()` 讀取並還原設定
- [ ] 7.3 在頁面載入時自動還原預警設定

## 8. Email 通知

- [ ] 8.1 新增 Email 設定 UI（Modal 或滑出面板）
- [ ] 8.2 實作 SMTP 設定驗證（傳送測試郵件）
- [ ] 8.3 實作通知開關（啟用/停用）

## 9. 測試與除錯

- [ ] 9.1 手動測試：新增低於下限規則，驗證預警觸發
- [ ] 9.2 手動測試：匯出歷史為 CSV
- [ ] 9.3 手動測試：Tab 紅點提示顯示正確
- [ ] 9.4 驗證 localStorage 1000 筆限制
