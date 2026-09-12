import os
from playwright.sync_api import sync_playwright

def render():
    base_dir = "/Users/goya/Documents/Antigravity/教会チラシ制作/04_本部被害報告アンケート_チラシ"
    html_path = os.path.join(base_dir, "index.html")
    file_url = f"file://{html_path}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. 全体高解像度画像（flyer_image.png）
        page = browser.new_page(viewport={"width": 1200, "height": 1600}, device_scale_factor=2)
        page.goto(file_url)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        flyer_elem = page.locator(".flyer")
        flyer_elem.screenshot(path=os.path.join(base_dir, "flyer_image.png"))
        print("✓ flyer_image.png generated")
        page.close()
        
        # 2. A4印刷PDF（flyer_a4.pdf）
        page_pdf = browser.new_page()
        page_pdf.goto(file_url)
        page_pdf.wait_for_load_state("networkidle")
        page_pdf.wait_for_timeout(1000)
        page_pdf.pdf(
            path=os.path.join(base_dir, "flyer_a4.pdf"),
            format="A4",
            print_background=True,
            margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
            prefer_css_page_size=True
        )
        print("✓ flyer_a4.pdf generated")
        page_pdf.close()
        
        # 3. 印刷エミュレーションプレビュー（print_preview.png）
        page_print = browser.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=2)
        page_print.emulate_media(media="print")
        page_print.goto(file_url)
        page_print.wait_for_load_state("networkidle")
        page_print.wait_for_timeout(1000)
        page_print.screenshot(path=os.path.join(base_dir, "print_preview.png"), full_page=False)
        print("✓ print_preview.png generated")
        page_print.close()
        
        # 4. スマホ表示プレビュー（preview_mobile.png）
        page_mob = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        page_mob.goto(file_url)
        page_mob.wait_for_load_state("networkidle")
        page_mob.wait_for_timeout(1000)
        page_mob.screenshot(path=os.path.join(base_dir, "preview_mobile.png"), full_page=True)
        print("✓ preview_mobile.png generated")
        page_mob.close()
        
        browser.close()

if __name__ == "__main__":
    render()
