import flet as ft
import json
import re
import requests
import os
from dotenv import load_dotenv 


load_dotenv()

# Firebase Config
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY")
FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
FIREBASE_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
FIREBASE_RESET_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"

def main(page: ft.Page):
    page.title = "Login / Sign up"
    page.window_width = 440
    page.window_height = 800
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # Controls
    email = ft.TextField(label="Email", width=350, border_radius=10)
    password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=350, border_radius=10)

    signup_email = ft.TextField(label="Email", width=350, border_radius=10)
    signup_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=350, border_radius=10)
    signup_confirm = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True, width=350, border_radius=10)

    forgot_email = ft.TextField(label="Enter your registered Email", width=350, border_radius=10)

    # Views
    login_view = ft.Container()
    signup_view = ft.Container()
    forgot_view = ft.Container()
    after_view = ft.Container()
    dashboard_view =ft.Container()

    sidebar_expanded = False
   # sidebar_container = ft.Container()
    

    def toggle_sidebar(e):
        nonlocal sidebar_expanded
        sidebar_expanded = not sidebar_expanded
        sidebar_container.visible = sidebar_expanded
        page.update()   

    def flip_to(view):
        for v in [login_view, signup_view, forgot_view,after_view,dashboard_view]:
            v.visible = False
        view.visible = True
        page.update()

    def validate_email(email_str):
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email_str))

    def show_alert(message):
        alert = ft.SnackBar(ft.Text(message, color=ft.Colors.WHITE))
        page.snack_bar = alert
        page.update()
        alert.open = True
        page.update()

    def submit_login(e):
        if not email.value or not validate_email(email.value):
            show_alert("Invalid email address!")
            return
        try:
            response = requests.post(FIREBASE_SIGNIN_URL, json={
                "email": email.value,
                "password": password.value,
                "returnSecureToken": True
            })
            res_data = response.json()
            if "error" in res_data:
                show_alert(res_data["error"]["message"])
            else:
                show_alert("Login successful!")
                flip_to(after_view)
                print(json.dumps(res_data, indent=2))
        except Exception as ex:
            show_alert(str(ex))

    def submit_signup(e):
        if not signup_email.value or not validate_email(signup_email.value):
            show_alert("Invalid email address!")
            return
        if signup_password.value != signup_confirm.value:
            show_alert("Passwords do not match!")
            return
        try:
            response = requests.post(FIREBASE_SIGNUP_URL, json={
                "email": signup_email.value,
                "password": signup_password.value,
                "returnSecureToken": True
            })
            res_data = response.json()
            if "error" in res_data:
                show_alert(res_data["error"]["message"])
            else:
                show_alert("Signup successful!")
                print(json.dumps(res_data, indent=2))
                flip_to(login_view)
        except Exception as ex:
            show_alert(str(ex))

    def submit_forgot(e):
        if not forgot_email.value or not validate_email(forgot_email.value):
            show_alert("Enter a valid email!")
            return
        try:
            response = requests.post(FIREBASE_RESET_URL, json={
                "requestType": "PASSWORD_RESET",
                "email": forgot_email.value
            })
            res_data = response.json()
            if "error" in res_data:
                show_alert(res_data["error"]["message"])
            else:
                show_alert("Reset link sent to your email!")
                print(json.dumps(res_data, indent=2))
        except Exception as ex:
            show_alert(str(ex))

    def social_login(provider):
        show_alert(f"{provider} login not implemented.")
        print(json.dumps({"social_login": provider}, indent=2))

    def social_button(name, icon_url, bg, fg, on_click):
        return ft.ElevatedButton(
            content=ft.Row([
                ft.Image(src=icon_url, width=20, height=20),
                ft.Text(f"Continue with {name}", size=16, weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            style=ft.ButtonStyle(
                bgcolor=bg,
                color=fg,
                shape=ft.RoundedRectangleBorder(radius=15),
                padding=15,
                elevation=3
            ),
            on_click=on_click,
            expand=True
        )

    # Dark mode toggle
    dark_mode_icon = ft.IconButton(icon=ft.icons.MOOD, icon_size=30)

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            dark_mode_icon.icon = ft.icons.MOOD_OUTLINED
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            dark_mode_icon.icon = ft.icons.MOOD
        page.update()

    dark_mode_icon.on_click = toggle_theme


    sidebar_container = ft.Container(
        content=ft.Column([ 
            ft.Container(content=ft.Row([ft.Icon(ft.icons.PERSON, color=ft.colors.BLACK), ft.Text("Account", weight="bold", size=16, color=ft.colors.BLACK)]), on_click=lambda _: flip_to(login_view), padding=5),
            ft.Container(content=ft.Row([ft.Icon(ft.icons.BAR_CHART, color=ft.colors.BLACK), ft.Text("Statistic", weight="bold", size=16, color=ft.colors.BLACK)]), on_click=lambda _: flip_to(login_view), padding=5),
            ft.Container(content=ft.Row([ft.Icon(ft.icons.SETTINGS, color=ft.colors.BLACK), ft.Text("Settings", weight="bold", size=16, color=ft.colors.BLACK)]), on_click=lambda _: flip_to(login_view), padding=5),
            ft.Container(content=ft.Row([ft.Icon(ft.icons.EXIT_TO_APP, color=ft.colors.BLACK), ft.Text("Logout", weight="bold", size=16, color=ft.colors.BLACK)]), on_click=lambda _: flip_to(login_view), padding=5),
        ], spacing=10),
        width=150,
        height=200,
        border=ft.border.all(1, ft.colors.BLACK),
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        padding=10,
        visible=False,  # Initially hidden
    )


    def stat_card(title, value, icon, color):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=ft.colors.WHITE),
                    ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text(title, size=14, color=ft.colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=100,
            height=110,
            padding=10,
            bgcolor=color,
            border_radius=15
        )
    
    dashboard_view = ft.Container()
    top_row = ft.Row([ft.IconButton(icon=ft.icons.MENU, tooltip="Menu", icon_color=ft.colors.BLACK,on_click=toggle_sidebar), ft.Container(expand=True), ft.IconButton(icon=ft.icons.MESSAGE_ROUNDED,
     tooltip="Contact", icon_color=ft.colors.BLACK,)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    
    dashboard_view = ft.Container(
        content=ft.Column(
            [
                top_row,
                ft.Divider(height=1, color=ft.colors.GREY),  # Optional: horizontal line below top bar
                ft.Text("Welcome to the Dashboard!", size=24, weight=ft.FontWeight.BOLD),
                # Add more widgets/content here
            ],
            spacing=20,
            expand=True
        ),
        padding=20
    )

    dashboard_view.visible = False


    after_view = ft.Container(ft.Column(
        [
            # Profile Section
            ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src="assets/image.png",  
                            width=100,
                            height=100,
                            border_radius=50,
                            fit=ft.ImageFit.COVER
                        ),
                        ft.Text("Thilac .R", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Undergraduate student", size=14, color=ft.colors.GREY),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                alignment=ft.alignment.center,
                padding=20
            ),

            # Stats Section
            ft.Container(
                content=ft.Row(
                    [
                        stat_card("Wins", "25", ft.icons.EMOJI_EVENTS, ft.colors.GREEN_300),
                        stat_card("Scores", "1200", ft.icons.SCORE, ft.colors.BLUE_300),
                        stat_card("Rank", "Gold", ft.icons.MILITARY_TECH, ft.colors.AMBER_300),
                        #stat_card("Rank", "Silver", ft.icons.MILITARY_TECH, ft.colors.GREY_300),
                        #stat_card("Rank", "Bronze", ft.icons.MILITARY_TECH, ft.colors.AMBER),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                padding=10
            ),

            # History & Location
            ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.HISTORY),
                            title=ft.Text("Last 5 Debates"),
                            subtitle=ft.Text("W W L W W")
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.LOCATION_ON),
                            title=ft.Text("Location"),
                            subtitle=ft.Text("Colombo, Sri Lanka")
                        )
                    ]
                ),
                padding=10,
                bgcolor=ft.colors.GREY_100,
                border_radius=10,
                margin=10
            ),

            # Action
            ft.Row(
                [
                    ft.ElevatedButton(
                        text="Back",
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: flip_to(dashboard_view)
                    ),
                    ft.OutlinedButton(
                        text="Log out",
                        icon=ft.icons.LOGOUT_ROUNDED,
                        on_click=lambda _: flip_to(login_view)
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    ),width=400,border_radius=25,bgcolor=ft.Colors.WHITE,shadow=ft.BoxShadow,border=ft.border.all(1, ft.colors.BLACK),padding=10)
    
    after_view.width = 400
    after_view.border_radius = 25
    after_view.bgcolor = ft.Colors.WHITE
    after_view.shadow = ft.BoxShadow(blur_radius=30, color=ft.Colors.BLACK12, offset=ft.Offset(4, 4))
    after_view.visible = False

    

    
    

    # Login View
    login_view.content = ft.Column([
        ft.Row([dark_mode_icon], alignment=ft.MainAxisAlignment.END),
        ft.Text("Login", size=30, weight=ft.FontWeight.BOLD, text_align="center"),
        email,
        password,
        ft.ElevatedButton("Login", on_click=submit_login, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), padding=15), expand=True),
        ft.Text("Or login using:", size=14, italic=True),
        social_button("Google", "https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg", ft.Colors.WHITE, ft.Colors.BLACK, lambda e: social_login("Google")),
        social_button("Apple", "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg", ft.Colors.WHITE, ft.Colors.BLACK, lambda e: social_login("Apple")),
        social_button("GitHub", "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg", ft.Colors.BLUE_GREY_900, ft.Colors.WHITE, lambda e: social_login("GitHub")),
        ft.Row([
            ft.TextButton("Forgot Password?", on_click=lambda _: flip_to(forgot_view)),
            ft.TextButton("Sign Up", on_click=lambda _: flip_to(signup_view))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    login_view.padding = 30
    login_view.width = 400
    login_view.border_radius = 25
    login_view.bgcolor = ft.Colors.WHITE
    login_view.shadow = ft.BoxShadow(blur_radius=30, color=ft.Colors.BLACK12, offset=ft.Offset(4, 4))
    login_view.visible = True

    # Sign Up View
    signup_view.content = ft.Column([
        ft.Text("Sign Up", size=30, weight=ft.FontWeight.BOLD),
        signup_email,
        signup_password,
        signup_confirm,
        ft.ElevatedButton("Create Account", on_click=submit_signup),
        ft.TextButton("Back to Login", on_click=lambda _: flip_to(login_view))
    ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    signup_view.padding = 30
    signup_view.width = 400
    signup_view.border_radius = 25
    signup_view.bgcolor = ft.Colors.WHITE
    signup_view.shadow = ft.BoxShadow(blur_radius=30, color=ft.Colors.BLACK12, offset=ft.Offset(4, 4))
    signup_view.visible = False

    # Forgot Password View
    forgot_view.content = ft.Column([
        ft.Text("Forgot Password", size=30, weight=ft.FontWeight.BOLD),
        forgot_email,
        ft.ElevatedButton("Send Reset Link", on_click=submit_forgot),
        ft.TextButton("Back to Login", on_click=lambda _: flip_to(login_view))
    ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    forgot_view.padding = 30
    forgot_view.width = 400
    forgot_view.border_radius = 25
    forgot_view.bgcolor = ft.Colors.WHITE
    forgot_view.shadow = ft.BoxShadow(blur_radius=30, color=ft.Colors.BLACK12, offset=ft.Offset(4, 4))
    forgot_view.visible = False

    # Add all views to the page
    page.add(
        #ft.Row([ft.Icon(ft.Icons.MIC_EXTERNAL_ON_OUTLINED,color=ft.Colors.BLACK, size=30),ft.Text("Vivaathi", size=30, weight=ft.FontWeight.BOLD, text_align="center")], alignment=ft.MainAxisAlignment.END),
        
        ft.Stack([
            login_view,
            signup_view,
            forgot_view,
            after_view,
            dashboard_view,
        ])
    )

ft.app(target=main)
