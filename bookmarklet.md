# Ghost AI Blog Generator - Bookmarklet

## Quick Install (30 seconds)

### Step 1: Copy this code
```javascript
javascript:(function(){var d=document,s=d.createElement('div');s.innerHTML='<style>.ai-modal{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);z-index:999999;display:flex;align-items:center;justify-content:center}.ai-box{background:#fff;padding:30px;border-radius:10px;width:500px;max-width:90%}.ai-close{float:right;font-size:24px;cursor:pointer;color:#999}.ai-input,.ai-select{width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:5px;box-sizing:border-box}.ai-btn{width:100%;padding:12px;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;border-radius:5px;cursor:pointer;font-size:16px}</style><div class="ai-modal"><div class="ai-box"><span class="ai-close" onclick="this.parentElement.parentElement.remove()">&times;</span><h2>Generate AI Blog Post</h2><input class="ai-input" id="ai-topic" placeholder="Blog topic..."><select class="ai-select" id="ai-model"><option value="llama-3.3-70b-versatile">Llama 3.3 70B</option><option value="llama-3.1-8b-instant">Llama 3.1 8B (Fast)</option></select><select class="ai-select" id="ai-status"><option value="draft">Draft</option><option value="published">Published</option></select><button class="ai-btn" onclick="(function(){var t=document.getElementById(\'ai-topic\').value,m=document.getElementById(\'ai-model\').value,s=document.getElementById(\'ai-status\').value;if(!t)return alert(\'Enter a topic\');fetch(\'https://ghost-ai.quapton.com/generate-blog\',{method:\'POST\',headers:{\'Content-Type\':\'application/json\'},body:JSON.stringify({topic:t,model:m,status:s})}).then(r=>r.json()).then(d=>{if(d.success){alert(\'Success! Post created: \'+d.title);window.open(d.post_url,\'_blank\');document.querySelector(\'.ai-modal\').remove()}else alert(\'Error: \'+d.error)}).catch(e=>alert(\'Error: \'+e))})()">Generate Post</button></div></div>';d.body.appendChild(s.firstChild)})();
```

### Step 2: Add to bookmarks
1. **Chrome/Edge**:
   - Show bookmarks bar: Ctrl+Shift+B (Windows) or Cmd+Shift+B (Mac)
   - Right-click bookmarks bar → "Add page..."
   - Name: "AI Blog Generator"
   - URL: Paste the code above
   - Click Save

2. **Firefox**:
   - Right-click bookmarks toolbar → "New Bookmark"
   - Name: "AI Blog Generator"
   - Location: Paste the code above
   - Click Add

3. **Safari**:
   - Bookmarks → Add Bookmark...
   - Name: "AI Blog Generator"
   - Address: Paste the code above
   - Click Add

## Usage

1. Go to Ghost Admin (any page)
2. Click the "AI Blog Generator" bookmark
3. Enter your topic
4. Select model & status
5. Click Generate
6. Opens new post when done!

## Features
- Works on ANY page (Ghost admin, editor, anywhere!)
- No installation needed
- Instant modal popup
- Direct link to generated post
- Mobile friendly

## Troubleshooting
- If nothing happens, check browser console for errors
- Ensure ghost-ai.quapton.com is accessible
- Try refreshing the page and clicking again