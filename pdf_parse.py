import fitz
import base64
import dashscope
from dashscope import MultiModalConversation
from config import API_KEY, QWEN_VISION_MODEL

dashscope.api_key = API_KEY

# ======================= 修复版：接收二进制 =======================
def img_describe(img_bytes):
    # 二进制转 base64，不需要路径！不会报错！
    base64_data = base64.b64encode(img_bytes).decode("utf-8")
    image_url = f"data:image/png;base64,{base64_data}"

    resp = MultiModalConversation.call(
        api_key=API_KEY,
        model=QWEN_VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"image": image_url},
                    {"text": "请详细描述这张图片里的内容"}
                ]
            }
        ]
    )
    if resp.status_code == 200:
        return resp.output.choices[0].message.content
    else:
        return f"错误：{resp.code} -> {resp.message}"

def extract_pdf(pdf_path, start=0, end=5):
    doc = fitz.open(pdf_path)
    full_text = ""
    print(f"✅ 开始解析 PDF，共 {doc.page_count} 页，处理前 {end-start} 页内容")

    for idx in range(start, min(end, doc.page_count)):
        page = doc.load_page(idx)
        print(f"正在处理第 {idx+1} 页...")

        page_imgs_raw = page.get_images(full=True)
        img_bbox_xref = {}
        for xref, *_ in page_imgs_raw:
            rect_list = page.get_image_rects(xref)
            for rect in rect_list:
                key = (round(rect.x0, 3), round(rect.y0, 3), round(rect.x1, 3), round(rect.y1, 3))
                img_bbox_xref[key] = xref

        blocks = page.get_text("dict")["blocks"]
        for blk in blocks:
            if blk["type"] == 0:
                txt = ""
                for line in blk["lines"]:
                    for span in line["spans"]:
                        txt += span["text"]
                full_text += txt + "\n"

            elif blk["type"] == 1:
                b = blk["bbox"]
                b_key = (round(b[0], 3), round(b[1], 3), round(b[2], 3), round(b[3], 3))
                if b_key in img_bbox_xref:
                    xref = img_bbox_xref[b_key]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.width > 80 and pix.height > 80:
                        img_bin = pix.tobytes("png")
                        desc = img_describe(img_bin)
                        full_text += f"\n【插图描述】{desc}\n"
                    pix = None

        full_text += "\n===== 第" + str(idx+1) + "页结束 =====\n"

    doc.close()
    print("✅ PDF 解析完成！")
    return full_text