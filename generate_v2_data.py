import pandas as pd
import numpy as np

def generate_v2_data(output_path):
    # 1. 月度數據 (擴充：情境模擬所需欄位，或更細的時間維度)
    months = [f"2024-{str(i).zfill(2)}" for i in range(1, 13)]
    monthly_data = pd.DataFrame({
        '時間': months,
        '銷售收入': [3850000, 3200000, 4100000, 4350000, 4700000, 5200000, 5600000, 5100000, 4450000, 4900000, 5800000, 6200000],
        '銷售成本': [2502500, 2112000, 2583000, 2784000, 2867000, 3172000, 3416000, 3213000, 3026000, 3136000, 3596000, 3782000]
    })
    monthly_data['毛利額'] = monthly_data['銷售收入'] - monthly_data['銷售成本']
    monthly_data['毛利率'] = monthly_data['毛利額'] / monthly_data['銷售收入']
    monthly_data['去年同期收入'] = monthly_data['銷售收入'] * np.random.uniform(0.85, 0.98, size=12) # YoY 分析
    monthly_data['去年同期成本'] = monthly_data['銷售成本'] * np.random.uniform(0.88, 0.99, size=12)

    # 2. 產品數據 (擴充：價格、銷量、成本，用於三維氣泡圖與模擬器)
    products_data = pd.DataFrame({
        '產品名稱': ['經典休閒外套', '時尚皮帶包', '機能運動鞋', '基本款棉T', '限量聯名夾克', '珍珠項鍊', '輕量慢跑鞋', '丹寧牛仔褲', '羊毛大衣', '帆布手提袋'],
        '類別': ['服飾類', '飾品類', '鞋類', '服飾類', '服飾類', '飾品類', '鞋類', '服飾類', '服飾類', '飾品類'],
        '銷售單價': [1500, 2200, 2800, 500, 4500, 3500, 2500, 1200, 6800, 950],
        '單位成本': [870, 1144, 1932, 360, 2160, 1575, 1775, 900, 3060, 520],
        '銷售總量': [1233, 545, 350, 1300, 466, 251, 304, 433, 150, 600]
    })
    products_data['毛利額'] = (products_data['銷售單價'] - products_data['單位成本']) * products_data['銷售總量']
    products_data['毛利率'] = (products_data['銷售單價'] - products_data['單位成本']) / products_data['銷售單價']
    
    total_rev = (products_data['銷售單價'] * products_data['銷售總量']).sum()
    products_data['銷售額'] = products_data['銷售單價'] * products_data['銷售總量']
    products_data['相對市占率'] = np.random.uniform(0.05, 0.35, size=10) # BCG X
    products_data['市場成長率'] = np.random.uniform(-0.1, 0.45, size=10) # BCG Y
    
    # 決定 BCG
    def assign_bcg(row):
        if row['市場成長率'] >= 0.15 and row['相對市占率'] >= 0.15: return '明星'
        if row['市場成長率'] < 0.15 and row['相對市占率'] >= 0.15: return '金牛'
        if row['市場成長率'] >= 0.15 and row['相對市占率'] < 0.15: return '問題兒'
        return '瘦狗'
    products_data['BCG象限'] = products_data.apply(assign_bcg, axis=1)

    # 3. 地域渠道
    regions_data = pd.DataFrame({
        '地區': ['台北', '台中', '高雄', '新竹', '台南', '桃園', '花蓮', '基隆', '竹北', '彰化'],
        '主要渠道': ['直銷', '直銷', '經銷', '直銷', '電商', '電商', '經銷', '電商', '直銷', '經銷'],
        '毛利率': [0.42, 0.39, 0.35, 0.41, 0.38, 0.395, 0.31, 0.36, 0.45, 0.33],
        '銷售額': [4200000, 2800000, 2100000, 1900000, 1600000, 1500000, 650000, 580000, 1200000, 850000],
        '物流成本率': [0.05, 0.06, 0.08, 0.05, 0.04, 0.04, 0.12, 0.05, 0.04, 0.07],
        '渠道ROI': [3.2, 2.8, 2.1, 3.0, 2.6, 2.9, 1.5, 2.2, 3.5, 1.8]
    })

    # 4. 成本結構 (擴充：樹狀圖用的大中小類)
    costs_data = pd.DataFrame({
        '成本大類': ['直接成本', '直接成本', '直接成本', '間接成本', '間接成本', '間接成本', '間接成本', '間接成本', '間接成本', '間接成本'],
        '成本小類': ['原材料採購', '直接人工', '物流運費', '廠房租金', '行銷廣告', '設備折舊', '管理薪資', '包裝材料', '品管費用', '雜項支出'],
        '屬性': ['可變', '可變', '可變', '固定', '可變', '固定', '固定', '可變', '可變', '固定'],
        '金額': [8540000, 3200000, 1850000, 1200000, 980000, 680000, 620000, 450000, 280000, 200000]
    })

    # 5. 客戶群體 (擴充 LTV 等級)
    customers_data = pd.DataFrame({
        '客戶名稱': ['台北旗艦大戶', '中山路經銷', '中友實體通路', '漢神VIP群', '神腦專戶', 'MOMO品牌館', '蝦皮優選', '台南東區直營', '花蓮散客群', '基隆網路店'],
        '區域': ['台北', '台北', '台中', '高雄', '新竹', '台灣', '台灣', '台南', '花蓮', '基隆'],
        'LTV總額': [1850000, 1420000, 980000, 860000, 620000, 1100000, 780000, 450000, 280000, 380000],
        '平均客單價': [12500, 9800, 8200, 7600, 5400, 6800, 5200, 4200, 3100, 3800],
        '月均頻率': [5.2, 4.8, 3.9, 3.5, 2.8, 6.2, 4.1, 2.2, 1.5, 2.0],
        '毛利貢獻率': [0.42, 0.40, 0.38, 0.36, 0.32, 0.39, 0.35, 0.30, 0.25, 0.28]
    })
    
    def assign_tier(ltv):
        if ltv >= 1000000: return 'VIP'
        if ltv >= 700000: return 'Premium'
        if ltv >= 400000: return 'Standard'
        return 'Basic'
    customers_data['客戶層級'] = customers_data['LTV總額'].apply(assign_tier)

    # 6. 促銷折扣
    promotions_data = pd.DataFrame({
        '活動代號': ['春節特賣', '週年慶', '雙11', '母親節', '開學季', '聖誕特惠', '618', '換季清倉'],
        '適用類別': ['服飾類', '飾品類', '全品類', '飾品類', '服飾類', '鞋類', '全品類', '服飾類'],
        '平均折扣率': [0.20, 0.30, 0.25, 0.15, 0.18, 0.22, 0.28, 0.40],
        '銷量增幅': [0.35, 0.55, 0.65, 0.25, 0.30, 0.28, 0.60, 0.80],
        '毛利影響點數': [-0.08, -0.12, -0.10, -0.05, -0.07, -0.09, -0.11, -0.18],
        '活動ROI': [1.8, 2.2, 2.8, 1.6, 1.9, 1.4, 2.5, 1.2]
    })

    # 將數據寫入 Excel
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        monthly_data.to_excel(writer, sheet_name='月度數據', index=False)
        products_data.to_excel(writer, sheet_name='產品數據', index=False)
        regions_data.to_excel(writer, sheet_name='地區數據', index=False)
        costs_data.to_excel(writer, sheet_name='成本數據', index=False)
        customers_data.to_excel(writer, sheet_name='客戶數據', index=False)
        promotions_data.to_excel(writer, sheet_name='促銷數據', index=False)

        # 自動調整欄寬
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            worksheet.set_column(0, 10, 15)

    print(f"Data generated at {output_path}")

if __name__ == "__main__":
    generate_v2_data(r"c:\Users\jamic\新增資料夾\Gross_Profit_Sample_Data_V2.0.xlsx")
