
# Adding CSS in Django: A Step-by-Step Guide

Adding CSS in Django involves several steps, including setting up a static files directory, creating your CSS files, and linking them to your templates. Here’s a step-by-step guide to help you:

## Step 1: Setting Up Static Files

1. **Create a Static Directory:**
   In your Django project, create a directory called `static` inside your app directory (or at the project level if you want to share static files across apps).

   ```arduino
   myproject/
       myapp/
           static/
               myapp/
                   css/
                       styles.css
   ```

   Note: The nested `myapp` directory inside static helps in organizing files by app, which is useful if you have multiple apps.

2. **Configure `settings.py`:**
   Ensure your `settings.py` has the following settings for static files:

   ```python
   STATIC_URL = '/static/'

   # If your static files are stored at the project level
   STATICFILES_DIRS = [
       BASE_DIR / "static",
   ]

   # If you're collecting static files for deployment
   STATIC_ROOT = BASE_DIR / "staticfiles"
   ```

## Step 2: Creating Your CSS File

Create a CSS file in the static directory you set up. For example, `styles.css`:

```css
/* static/myapp/css/styles.css */
body {
    background-color: #f0f0f0;
    font-family: Arial, sans-serif;
}
```

## Step 3: Linking CSS in Templates

To link your CSS file in a Django template, you need to load static files at the beginning of your template and then reference the CSS file.

1. **Load Static Files:**
   Add `{% load static %}` at the top of your template.

2. **Link the CSS File:**
   Use the `{% static 'path/to/css/file.css' %}` template tag to generate the URL for your CSS file.

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>My Django App</title>
       {% load static %}
       <link rel="stylesheet" type="text/css" href="{% static 'myapp/css/styles.css' %}">
   </head>
   <body>
       <h1>Welcome to My Django App</h1>
   </body>
   </html>
   ```

## Step 4: Running the Development Server

Run your Django development server to see the changes.

```sh
python manage.py runserver
```

## Step 5: Collecting Static Files for Deployment

When you’re ready to deploy your Django project, you need to collect all static files into a single directory using the `collectstatic` command.

```sh
python manage.py collectstatic
```

This command gathers all static files from each app’s `static` directory and places them in the `STATIC_ROOT` directory specified in your `settings.py`.

## Summary

1. Create a `static` directory in your app (or project).
2. Add your CSS files to the appropriate directory.
3. Load and link the CSS files in your templates using `{% load static %}` and `{% static 'path/to/css/file.css' %}`.
4. Run your development server to see the changes.
5. Use `collectstatic` for deployment.