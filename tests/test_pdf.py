from pdf_parse import extract_pdf

def test_extract_pdf():
    text = extract_pdf("MLbook.pdf", 0, 1)
    print("✅ 提取长度:", len(text))
    print("内容:", text[:200])

if __name__ == "__main__":
    test_extract_pdf()