# Ghost AI Blog Generator - Installation Guide

## Quick Installation (5 minutes)

### Step 1: Access Ghost Code Injection

1. Log in to your Ghost Admin panel at `https://ghost.quapton.com/ghost`
2. Navigate to **Settings** (⚙️ icon in sidebar)
3. Click on **Advanced**
4. Scroll to **Code Injection**

### Step 2: Add the Code

1. Open the file `ghost-code-injection.html` from this repository
2. Copy **ALL** the code (Ctrl+A, Ctrl+C or Cmd+A, Cmd+C)
3. Paste it into the **Site Header** field in Ghost Code Injection
4. Click **Save** at the bottom of the page

### Step 3: Test It

1. Go to any page on your Ghost site (frontend or admin)
2. You should see a **"✨ Generate AI Post"** button in the bottom-right corner
3. Click the button to open the modal
4. Enter a blog topic (e.g., "The Future of AI in Healthcare")
5. Select your preferred AI model
6. Choose Draft or Published
7. Click **Generate Post**
8. Wait 30-60 seconds for the AI to generate your post
9. Success! You'll see a link to view your new post

## Features

### Floating Button
- Always visible in bottom-right corner
- Beautiful gradient design
- Hover animation
- Mobile responsive

### Modal Form
- Clean, modern design
- Topic input field
- AI model selection:
  - Llama 3.3 70B (Recommended)
  - Llama 3.1 8B (Fast)
  - Llama 4 Maverick
  - Llama 4 Scout
  - GPT-OSS 120B
  - Qwen3 32B
- Draft/Published status selector
- Real-time status updates
- Loading indicator
- Success/error messages
- Direct link to created post

### Smart Behavior
- Works on all Ghost pages (frontend and admin)
- Closes on clicking outside modal
- Closes on clicking X button
- Form resets after submission
- Disabled submit button during generation
- Comprehensive error handling

## Customization

### Change Button Position
Edit the `.ghost-ai-button` CSS:
```css
.ghost-ai-button {
  bottom: 20px;  /* Change this */
  right: 20px;   /* Change this */
  /* left: 20px; for left side */
}
```

### Change Button Text
Find this line:
```html
<button class="ghost-ai-button" id="ghostAiButton">✨ Generate AI Post</button>
```
Change to:
```html
<button class="ghost-ai-button" id="ghostAiButton">🤖 AI Writer</button>
```

### Change Colors
Edit the gradient in CSS:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Try these alternatives:
- Blue: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- Green: `linear-gradient(135deg, #00b09b 0%, #96c93d 100%)`
- Orange: `linear-gradient(135deg, #f093fb 0%, #f5576c 100%)`
- Purple: `linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)`

### Change Default Model
Find this line:
```html
<option value="llama-3.3-70b-versatile">Llama 3.3 70B (Recommended)</option>
```
Add `selected` attribute to your preferred model:
```html
<option value="llama-3.1-8b-instant" selected>Llama 3.1 8B (Fast)</option>
```

## Troubleshooting

### Button Not Appearing
1. Check that you pasted code in **Site Header** (not Site Footer)
2. Click Save in Ghost Code Injection
3. Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)
4. Clear browser cache

### Modal Not Opening
1. Check browser console for JavaScript errors (F12)
2. Ensure code was pasted completely
3. Try different browser

### API Errors
1. Verify `ghost-ai.quapton.com` is accessible
2. Check that AI service is running: `kubectl get pods -n ghost-ai`
3. Check service logs: `kubectl logs -n ghost-ai deployment/ghost-ai-service`
4. Verify Vault secrets are configured correctly

### Network Errors
1. Check browser network tab (F12 → Network)
2. Verify CORS is not blocking requests
3. Ensure HTTPS is working on ghost-ai.quapton.com

### Slow Generation
- Normal generation time: 30-60 seconds
- Larger models (70B, 120B) are slower but better quality
- Use Llama 3.1 8B for faster generation

## Uninstallation

To remove the AI blog generator:

1. Go to Ghost Admin → Settings → Advanced → Code Injection
2. Delete all code from the Site Header field
3. Click Save
4. Refresh any open Ghost pages

## Support

For issues or questions:
- Check service status: `kubectl get all -n ghost-ai`
- View service logs: `kubectl logs -n ghost-ai -l app=ghost-ai-service`
- Test API directly: `curl -X POST https://ghost-ai.quapton.com/generate-blog -H "Content-Type: application/json" -d '{"topic":"Test"}'`

## Security Note

The code injection runs on your Ghost site and makes API calls to your self-hosted AI service at `ghost-ai.quapton.com`. All data stays within your infrastructure. No third-party services are used except GroqCloud API for AI generation.