import easyocr
import re
import os

# OCRリーダー（日本語＋英語対応）
reader = easyocr.Reader(['ja', 'en'])

# スクリーンショット画像ファイル名（例：screenshot.png）
image_path = 'screenshot.png'  # あなたのスクショファイル名に変更

# OCR実行
text_lines = reader.readtext(image_path, detail=0)
text = '\n'.join(text_lines)

# --- 抽出ロジック例 ---
def extract_amount(text):
    match = re.search(r'¥?\s?[\d,]+円?', text)
    return match.group() if match else '未検出'

def extract_date(text):
    match = re.search(r'\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{4}年\d{1,2}月\d{1,2}日', text)
    return match.group() if match else '未検出'

def extract_address(text):
    match = re.search(r'〒\d{3}-\d{4}.*', text)
    return match.group() if match else '未検出'

def extract_doc_type(text):
    for keyword in ['請求書', '領収書', '納品書', '確定申告書']:
        if keyword in text:
            return keyword
    return '未検出'

# --- 結果出力 ---
amount = extract_amount(text)
date = extract_date(text)
address = extract_address(text)
doc_type = extract_doc_type(text)

# 出力（手動でコピーしやすい形に整形）
print("\n--- 抽出されたテキスト ---")
print(f"書類種類: {doc_type}")
print(f"金額: {amount}")
print(f"日付: {date}")
print(f"住所: {address}")
print(f"\n全文: {text}")

# --- CSV出力（オプション）---
# pandasを使ってCSVファイルに保存することもできますが、今回は手動でコピーする形にします。
# result = {
#     '金額': amount,
#     '日付': date,
#     '住所': address,
#     '書類名': doc_type,
#     '全文': text
# }
# df = pd.DataFrame([result])
# df.to_csv('抽出結果.csv', index=False, encoding='utf-8-sig')
# print("\n抽出結果を '抽出結果.csv' に保存しました。")
