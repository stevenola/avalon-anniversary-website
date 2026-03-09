import base64
import urllib.request
from pathlib import Path

def get_base64_image(url_or_path):
    try:
        if url_or_path.startswith('http'):
            with urllib.request.urlopen(url_or_path, timeout=10) as response:
                if response.status == 200:
                    content_type = response.info().get_content_type()
                    content = response.read()
                    return f'data:{content_type};base64,' + base64.b64encode(content).decode('utf-8')
        else:
            path = Path(url_or_path)
            if path.exists():
                content = path.read_bytes()
                ext = path.suffix[1:] if path.suffix else 'png'
                return f'data:image/{ext};base64,' + base64.b64encode(content).decode('utf-8')
    except Exception as e:
        pass
    return url_or_path

def generate_standalone():
    html_path = Path('/Users/stephenfingerman/Documents/Avalon Anniversary/Website revision/index.html')
    css_path = Path('/Users/stephenfingerman/Documents/Avalon Anniversary/Website revision/style.css')
    
    html_content = html_path.read_text()
    css_content = css_path.read_text()
    
    # Inline CSS
    html_content = html_content.replace('<link rel="stylesheet" href="style.css">', f'<style>\n{css_content}\n</style>')
    
    # Inline Local Images
    logo_path = '/Users/stephenfingerman/Documents/Avalon Anniversary/Website revision/assets/logo.png'
    logo_b64 = get_base64_image(logo_path)
    html_content = html_content.replace('src="assets/logo.png"', f'src="{logo_b64}"')
    
    # Inline CSS Unsplash Images
    hero_url = 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&q=80&w=2070'
    hero_b64 = get_base64_image(hero_url)
    html_content = html_content.replace(f"url('{hero_url}')", f"url('{hero_b64}')")
    
    service_url = 'https://images.unsplash.com/photo-1556740758-90de374c12ad?auto=format&fit=crop&q=80&w=2070'
    service_b64 = get_base64_image(service_url)
    html_content = html_content.replace(f"url('{service_url}')", f"url('{service_b64}')")
    
    output_path = Path('/Users/stephenfingerman/Documents/Avalon Anniversary/Website revision/avalon-standalone.html')
    output_path.write_text(html_content)
    print(f'Done: {output_path}')

if __name__ == "__main__":
    generate_standalone()
