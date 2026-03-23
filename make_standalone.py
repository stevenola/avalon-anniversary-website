import base64
import urllib.request
from pathlib import Path

BASE_DIR = Path('/Users/stephenfingerman/Documents/Avalon Anniversary/Website revision')

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
                ext = path.suffix[1:].lower() if path.suffix else 'png'
                if ext == 'jpg':
                    ext = 'jpeg'
                return f'data:image/{ext};base64,' + base64.b64encode(content).decode('utf-8')
    except Exception as e:
        print(f"Warning: Could not process image {url_or_path}: {e}")
    return url_or_path

def inline_images(html_content, css_content):
    """Inline all images (local and remote) into base64"""
    
    # Local asset images (in HTML)
    local_images = [
        ('assets/logo.png', 'src="assets/logo.png"', 'src="{}"'),
        ('assets/Avalon_30th_Badge_transparent_512.png', 'src="assets/Avalon_30th_Badge_transparent_512.png"', 'src="{}"'),
        ('assets/steve.png', 'src="assets/steve.png"', 'src="{}"'),
        ('assets/katie.png', 'src="assets/katie.png"', 'src="{}"'),
        ('assets/kelly.png', 'src="assets/kelly.png"', 'src="{}"'),
    ]
    
    for filename, search, replace_template in local_images:
        filepath = BASE_DIR / filename
        if filepath.exists():
            b64 = get_base64_image(str(filepath))
            html_content = html_content.replace(search, replace_template.format(b64))
    
    # Local hero images (in CSS)
    local_css_images = [
        'assets/hero-homepage.png',
        'assets/hero-services.png',
        'assets/hero-team.png',
        'assets/hero-testimonials.png',
        'assets/hero-contact.png',
        'assets/services-section-panel.png',
    ]
    
    for filename in local_css_images:
        filepath = BASE_DIR / filename
        if filepath.exists():
            b64 = get_base64_image(str(filepath))
            css_content = css_content.replace(f"url('{filename}')", f"url('{b64}')")
    
    # Remote Unsplash images (used in inline styles - keeping for any remaining references)
    remote_images = [
        'https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&q=80&w=2070',
        'https://images.unsplash.com/photo-1556740758-90de374c12ad?auto=format&fit=crop&q=80&w=2070',
        'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&q=80&w=800',
        'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&q=80&w=800',
        'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&q=80&w=800',
    ]
    
    for url in remote_images:
        b64 = get_base64_image(url)
        html_content = html_content.replace(f"url('{url}')", f"url('{b64}')")
        css_content = css_content.replace(f"url('{url}')", f"url('{b64}')")
    
    return html_content, css_content

def generate_standalone_page(html_filename, output_filename):
    """Generate a standalone HTML file with inlined CSS and images"""
    html_path = BASE_DIR / html_filename
    css_path = BASE_DIR / 'style.css'
    
    if not html_path.exists():
        print(f"Skipping {html_filename} - file not found")
        return
    
    html_content = html_path.read_text()
    css_content = css_path.read_text()
    
    # Inline images
    html_content, css_content = inline_images(html_content, css_content)
    
    # Inline CSS
    html_content = html_content.replace('<link rel="stylesheet" href="style.css">', f'<style>\n{css_content}\n</style>')
    
    output_path = BASE_DIR / output_filename
    output_path.write_text(html_content)
    print(f'Generated: {output_filename}')

def generate_all_standalone():
    """Generate standalone versions of all pages"""
    pages = [
        ('index.html', 'avalon-standalone.html'),
        ('services.html', 'services-standalone.html'),
        ('team.html', 'team-standalone.html'),
        ('testimonials.html', 'testimonials-standalone.html'),
        ('contact.html', 'contact-standalone.html'),
        ('thank-you.html', 'thank-you-standalone.html'),
    ]
    
    for html_file, output_file in pages:
        generate_standalone_page(html_file, output_file)
    
    print("\nAll standalone pages generated!")

if __name__ == "__main__":
    generate_all_standalone()
