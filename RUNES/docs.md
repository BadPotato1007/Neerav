# RUNES HTML Template Documentation

## about.html
- **Purpose:** The "About" page for the site.
- **Structure:** 
  - Uses Tailwind CSS and a custom "norse" font.
  - Gradient background with a sidebar containing the site logo and navigation.
  - The main content area is for "About" information (actual content may be below the snippet).
  - Sidebar and nav use frosted glass style effects.

## contact.html
- **Purpose:** The contact page for users to reach out.
- **Structure:** 
  - Similar styling as about.html (sidebar, frosted glass, Tailwind).
  - Sidebar contains navigation links like Home, About, etc.
  - Main area intended for contact information or a contact form.

## index.html
- **Purpose:** Main homepage/dashboard after login.
- **Structure:** 
  - Sidebar with logo and navigation.
  - Background image with gradient overlay.
  - Custom fonts/styles for branding.
  - Main content likely shows user information or dashboard widgets.

## leaderboard.html
- **Purpose:** Displays the leaderboard (likely for quiz or trivia results).
- **Structure:** 
  - Sidebar navigation (same branding as other pages).
  - Main area designed to show user rankings, scores, etc.

## login.html
- **Purpose:** Login form for users.
- **Structure:** 
  - Centered login form using Tailwind and frosted glass design.
  - Custom JavaScript for submitting login data via fetch to `/api/login`.
  - Navbar at the top with logo and site title.
  - Prominent branding and modern UI.

## quiz1.html & quiz_main.html
- **Purpose:** Main entry and subject selection for quizzes.
- **Structure:** 
  - Sidebar navigation, frosted glass, and branding.
  - Main area for quiz subject buttons (e.g., Physics).
  - JavaScript for redirecting to quiz page for the selected subject.

## signup.html
- **Purpose:** Account creation/signup form.
- **Structure:** 
  - Centered signup form styled with Tailwind and frosted glass.
  - Navbar with logo and site title.
  - Fields for username, email, and password.

---

### Shared Design Features
- All templates use:
  - Tailwind CSS for layout and utility classes.
  - Custom "norse" and "Quicksand" fonts.
  - Background images and gradient overlays.
  - "Frosted glass" effects for modern UI feel.
  - Responsive layouts for different devices.
  - Sidebar navigation with logo and site branding.




# Function Documentation for RUNES/apprunnerv2.py

## home()
- Route: '/'
- Purpose: Checks if a user is logged in by reading the username cookie. If the user is logged in, renders the homepage. If not, redirects to the signup page.

## login_page()
- Route: '/login' (GET)
- Purpose: Renders the login page template.

## contact()
- Route: '/contact' (GET)
- Purpose: Renders the contact page template.

## about()
- Route: '/about' (GET)
- Purpose: Renders the about page template.

## signup_page()
- Route: '/signup' (GET)
- Purpose: Renders the signup page template.

## signup()
- Route: '/api/signup' (POST)
- Purpose: Handles new user registration. Receives JSON data for username, password, and email. Inserts the new user into the userdata table in the database. Returns an error if username already exists.

## login()
- Route: '/api/login' (POST)
- Purpose: Authenticates a user. Receives username and password from POST JSON, checks database for matching credentials, and sets a cookie if successful.

## trivia_start()
- Route: '/trivia_start'
- Purpose: Checks if a user is logged in (via cookie). If not, redirects to login. Otherwise, renders the quiz main page.

## logout()
- Route: '/logout'
- Purpose: Logs out the user by deleting the username cookie and redirecting to the login page.

## profile()
- Route: '/api/profile' (GET)
- Purpose: Gets the profile info for the currently logged in user (from the cookie). If the user is not logged in, returns an error. Otherwise, fetches the username from the database.

## register()
- Route: '/api/register' (POST)
- Purpose: The code for this function is not fully visible in the retrieved results, but given the naming, it is likely to handle some form of user registration (potentially similar to /api/signup).