
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Mesh
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

import math
import os
import datetime
import json
import threading
from vosk import Model, KaldiRecognizer
import pyaudio
import platform
from plyer import gps
import vosk

# Phone-like testing size on laptop
Window.size = (400, 800)


class WaveBackground(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(
            size=self.update_waves,
            pos=self.update_waves
        )

        with self.canvas.before:

            # Main deep navy background
            Color(0.035, 0.065, 0.16, 1)

            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size
            )

            # First wave
            Color(0.07, 0.09, 0.24, 1)

            self.wave1 = Mesh(
                mode="triangles"
            )

            # Second wave
            Color(0.10, 0.12, 0.30, 1)

            self.wave2 = Mesh(
                mode="triangles"
            )

            # Third wave
            Color(0.16, 0.12, 0.40, 1)

            self.wave3 = Mesh(
                mode="triangles"
            )

    def make_wave(self, height, amplitude, phase):

        width = self.width + 5
        bottom = 0

        points = []

        steps = 40

        for i in range(steps + 1):

            x = width * i / steps

            y = height + amplitude * math.sin(
                (i / steps) * math.pi * 2 + phase
            )

            points.append((x, y))

        vertices = []

        # Top points
        for x, y in points:
            vertices.extend([x, y])

        # Bottom points
        for x, y in points:
            vertices.extend([x, bottom])

        indices = []

        for i in range(steps):

            top1 = i
            top2 = i + 1

            bottom1 = steps + 1 + i
            bottom2 = steps + 1 + i + 1

            indices.extend([
                top1,
                top2,
                bottom1,

                top2,
                bottom2,
                bottom1
            ])

        return vertices, indices

    def update_waves(self, *args):

        self.bg.pos = self.pos
        self.bg.size = self.size

        h = self.height + 5

        v1, i1 = self.make_wave(
            h * 0.27,
            h * 0.055,
            0
        )

        v2, i2 = self.make_wave(
            h * 0.20,
            h * 0.045,
            1.3
        )

        v3, i3 = self.make_wave(
            h * 0.14,
            h * 0.035,
            2.4
        )

        self.wave1.vertices = v1
        self.wave1.indices = i1

        self.wave2.vertices = v2
        self.wave2.indices = i2

        self.wave3.vertices = v3
        self.wave3.indices = i3


class CreateAccountScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()
        # SafeHER Logo
        logo_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "safeherlogo.png"
        )

        logo = Image(
            source=logo_path,
            size_hint=(0.22, 0.13),
            pos_hint={"x": 0.04, "top": 0.97},
            allow_stretch=True,
            keep_ratio=True
        )

        layout.add_widget(logo)

        # Heading
        title = Label(
            text="[b]Create Account[/b]",
            markup=True,
            font_size=dp(32),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.10),
            pos_hint={"center_x": 0.5, "top": 0.88}
        )
        layout.add_widget(title)

        # Full Name
        name = TextInput(
            hint_text="Full Name",
            multiline=False,
            size_hint=(0.80, 0.075),
            pos_hint={"center_x": 0.5, "top": 0.72},
            background_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)]
        )
        layout.add_widget(name)
        self.name_input = name

        # Email
        email = TextInput(
            hint_text="Email",
            multiline=False,
            size_hint=(0.80, 0.075),
            pos_hint={"center_x": 0.5, "top": 0.61},
            background_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)]
        )
        layout.add_widget(email)

        # Password
        password = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint=(0.80, 0.075),
            pos_hint={"center_x": 0.5, "top": 0.50},
            background_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)]
        )
        layout.add_widget(password)

        # Confirm Password
        confirm = TextInput(
            hint_text="Confirm Password",
            password=True,
            multiline=False,
            size_hint=(0.80, 0.075),
            pos_hint={"center_x": 0.5, "top": 0.39},
            background_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)]
        )
        layout.add_widget(confirm)

        # Create Account button
        create_button = Button(
            text="Create Account",
            font_size=dp(18),
            color=(1, 1, 1, 1),
            size_hint=(0.70, 0.085),
            pos_hint={"center_x": 0.5, "top": 0.26},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        with create_button.canvas.before:
            Color(0.48, 0.30, 0.95, 1)

            button_bg = RoundedRectangle(
                pos=create_button.pos,
                size=create_button.size,
                radius=[dp(35)]
            )

        def update_button(*args):
            button_bg.pos = create_button.pos
            button_bg.size = create_button.size

        create_button.bind(
            pos=update_button,
            size=update_button
        )

        layout.add_widget(create_button)

        def create_account_action(instance):
            if password.text == "" or confirm.text == "":
                print("Please enter password")

            elif password.text != confirm.text:
                print("Passwords do not match")

            else:
                print("Account created successfully")
                app = App.get_running_app()
                app.config.set("User", "full_name", self.name_input.text.strip())
                app.config.write()
                self.manager.current = "dashboard"

        create_button.bind(on_release=create_account_action)

        login_button = Button(
            text="Already have an account? Login",
            font_size=dp(15),
            color=(0.90, 0.90, 0.95, 1),
            size_hint=(1, 0.07),
            pos_hint={"center_x": 0.5, "top": 0.16},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        layout.add_widget(login_button)

        login_button.bind(
            on_release=lambda x: setattr(
                self.manager,
                "current",
                "login"
            )
        )

        self.add_widget(layout)


class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = WaveBackground()

        title = Label(
            text="[b]Welcome Back[/b]",
            markup=True,
            font_size=dp(32),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.10),
            pos_hint={"center_x": 0.5, "top": 0.82}
        )
        layout.add_widget(title)

        email = TextInput(
            hint_text="Email",
            multiline=False,
            size_hint=(0.80, 0.075),
            pos_hint={"center_x": 0.5, "top": 0.65},
            background_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)]
        )
        layout.add_widget(email)

        password = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint=(0.80, 0.075),
            pos_hint={"center_x": 0.5, "top": 0.53},
            background_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)]
        )
        layout.add_widget(password)

        login_button = Button(
            text="Login",
            font_size=dp(18),
            color=(1, 1, 1, 1),
            size_hint=(0.70, 0.085),
            pos_hint={"center_x": 0.5, "top": 0.37},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        with login_button.canvas.before:
            Color(0.48, 0.30, 0.95, 1)

            button_bg = RoundedRectangle(
                pos=login_button.pos,
                size=login_button.size,
                radius=[dp(35)]
            )

        def update_button(*args):
            button_bg.pos = login_button.pos
            button_bg.size = login_button.size

        login_button.bind(
            pos=update_button,
            size=update_button
        )

        layout.add_widget(login_button)

        signup_button = Button(
            text="Don't have an account? Create Account",
            font_size=dp(15),
            color=(0.90, 0.90, 0.95, 1),
            size_hint=(1, 0.07),
            pos_hint={"center_x": 0.5, "top": 0.27},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        layout.add_widget(signup_button)

        signup_button.bind(
            on_release=lambda x: setattr(
                self.manager,
                "current",
                "create_account"
            )
        )

        self.add_widget(layout)

class DashboardScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = WaveBackground()

        # SafeHER Logo
        logo_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "safeherlogo.png"
        )

        logo = Image(
            source=logo_path,
            size_hint=(0.22, 0.13),
            pos_hint={"x": 0.04, "top": 0.97},
            allow_stretch=True,
            keep_ratio=True
        )

        layout.add_widget(logo)

        # SafeHER heading
        title = Label(
            text="[b]SafeHER[/b]",
            markup=True,
            font_size=dp(32),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.08),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        layout.add_widget(title)

        # Safety status
        status = Label(
            text="[b]Safety Monitoring Active[/b]",
            markup=True,
            font_size=dp(19),
            color=(0.85, 0.85, 0.9, 1),
            size_hint=(1, 0.07),
            pos_hint={"center_x": 0.5, "top": 0.86}
        )
        layout.add_widget(status)

        # Voice detection status
        voice_status = Label(
            text="Voice Detection: Ready",
            font_size=dp(15),
            color=(0.75, 0.75, 0.82, 1),
            size_hint=(1, 0.05),
            pos_hint={"center_x": 0.5, "top": 0.81}
        )
        layout.add_widget(voice_status)

        # SOS Button
        sos_button = Button(
            text="[b]SOS[/b]\nPress in Emergency",
            markup=True,
            font_size=dp(22),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.85, 0.12, 0.25, 1),
            size_hint=(0.58, 0.20),
            pos_hint={"center_x": 0.5, "center_y": 0.57}
        )
        layout.add_widget(sos_button)
        sos_button.bind(
            on_release=lambda x: setattr(
                self.manager,
                "current",
                "sos_verification"
            )
        )

        # Information below SOS
        info = Label(
            text="Your safety controls are available below",
            font_size=dp(14),
            color=(0.75, 0.75, 0.82, 1),
            size_hint=(1, 0.06),
            pos_hint={"center_x": 0.5, "center_y": 0.43}
        )
        layout.add_widget(info)

        # Emergency Contacts
        contacts_button = Button(
            text="Emergency Contacts",
            font_size=dp(15),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.18, 0.16, 0.28, 1),
            size_hint=(0.40, 0.09),
            pos_hint={"center_x": 0.28, "center_y": 0.32}
        )
        layout.add_widget(contacts_button)
        contacts_button.bind(
            on_release=lambda x: setattr(
                self.manager,
                "current",
                "emergency_contacts"
            )
        )
        # Safety PIN
        pin_button = Button(
            text="Safety PIN",
            font_size=dp(15),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.18, 0.16, 0.28, 1),
            size_hint=(0.40, 0.09),
            pos_hint={"center_x": 0.72, "center_y": 0.32}
        )
        layout.add_widget(pin_button)

        def open_pin_screen(instance):
            app = App.get_running_app()
            saved_pin = app.config.get("Security", "pin")

            if saved_pin:
                self.manager.current = "verify_pin"
            else:
                self.manager.current = "safety_pin"

        pin_button.bind(
            on_release=open_pin_screen
        )
        # Safety Timer
        timer_button = Button(
            text="Safety Timer",
            font_size=dp(15),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.18, 0.16, 0.28, 1),
            size_hint=(0.40, 0.09),
            pos_hint={"center_x": 0.28, "center_y": 0.20}
        )
        layout.add_widget(timer_button)
        timer_button.bind(
            on_release=lambda x: setattr(
                self.manager,
                "current",
                "safety_timer"
            )
        )

        # Location
        location_button = Button(
            text="Location",
            font_size=dp(15),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.18, 0.16, 0.28, 1),
            size_hint=(0.40, 0.09),
            pos_hint={"center_x": 0.72, "center_y": 0.20}
        )
        layout.add_widget(location_button)
        location_button.bind(
            on_release=lambda x: setattr(
                self.manager,
                "current",
                "location"
            )
        )
        # Incident Timeline
        timeline_button = Button(
            text="Incident Timeline",
            font_size=dp(15),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.18, 0.16, 0.28, 1),
            size_hint=(0.40, 0.09),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.10
            }
        )

        layout.add_widget(timeline_button)

        timeline_button.bind(
            on_release=lambda x: setattr(
                self.manager,
                "current",
                "incident_timeline"
            )
        )

        # Add Dashboard layout ONCE
        self.add_widget(layout)

class LocationScreen(Screen):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.latitude = None
                self.longitude = None

                self.build_location_screen()

            def build_location_screen(self):

                self.clear_widgets()

                layout = WaveBackground()

                title = Label(
                    text="[b]Current Location[/b]",
                    markup=True,
                    font_size=dp(30),
                    color=(1, 1, 1, 1),
                    size_hint=(1, 0.10),
                    pos_hint={
                        "center_x": 0.5,
                        "top": 0.91
                    }
                )

                layout.add_widget(title)

                info = Label(
                    text=(
                        "GPS location will be obtained "
                        "directly from your device."
                    ),
                    font_size=dp(15),
                    color=(0.80, 0.80, 0.88, 1),
                    halign="center",
                    valign="middle",
                    size_hint=(0.88, 0.12),
                    pos_hint={
                        "center_x": 0.5,
                        "top": 0.80
                    }
                )

                info.bind(
                    size=lambda instance, value: setattr(
                        instance,
                        "text_size",
                        (instance.width, instance.height)
                    )
                )

                layout.add_widget(info)

                self.location_label = Label(
                    text="Location not available yet.",
                    font_size=dp(17),
                    color=(1, 1, 1, 1),
                    halign="center",
                    valign="middle",
                    size_hint=(0.90, 0.20),
                    pos_hint={
                        "center_x": 0.5,
                        "center_y": 0.55
                    }
                )

                self.location_label.bind(
                    size=lambda instance, value: setattr(
                        instance,
                        "text_size",
                        (instance.width, instance.height)
                    )
                )

                layout.add_widget(self.location_label)

                get_location_button = Button(
                    text="Get Current Location",
                    font_size=dp(18),
                    color=(1, 1, 1, 1),
                    background_normal="",
                    background_color=(0.48, 0.30, 0.95, 1),
                    size_hint=(0.70, 0.085),
                    pos_hint={
                        "center_x": 0.5,
                        "center_y": 0.34
                    }
                )

                layout.add_widget(get_location_button)

                get_location_button.bind(
                    on_release=self.start_gps
                )

                back_button = Button(
                    text="Back to Safety Dashboard",
                    font_size=dp(15),
                    color=(0.85, 0.85, 0.90, 1),
                    background_normal="",
                    background_color=(0, 0, 0, 0),
                    size_hint=(0.80, 0.07),
                    pos_hint={
                        "center_x": 0.5,
                        "center_y": 0.18
                    }
                )

                layout.add_widget(back_button)

                back_button.bind(
                    on_release=lambda instance:
                    setattr(
                        self.manager,
                        "current",
                        "dashboard"
                    )
                )

                self.add_widget(layout)

            def start_gps(self, instance):

                self.location_label.text = (
                    "Getting current location..."
                )

                try:

                    gps.configure(
                        on_location=self.on_location,
                        on_status=self.on_gps_status
                    )

                    gps.start(
                        minTime=1000,
                        minDistance=1
                    )

                    print(
                        "GPS started successfully"
                    )

                except Exception as error:

                    self.location_label.text = (
                        "GPS is not available on this device."
                    )

                    print(
                        "GPS error:",
                        error
                    )

            def on_location(
                    self,
                    **kwargs
            ):

                self.latitude = kwargs.get(
                    "lat"
                )

                self.longitude = kwargs.get(
                    "lon"
                )

                Clock.schedule_once(
                    self.update_location_text,
                    0
                )

            def update_location_text(self, dt):

                if (
                        self.latitude is not None
                        and self.longitude is not None
                ):
                    self.location_label.text = (
                        "[b]Current Location[/b]\n\n"
                        f"Latitude: {self.latitude}\n"
                        f"Longitude: {self.longitude}"
                    )

                    print(
                        "GPS Location:",
                        self.latitude,
                        self.longitude
                    )

            def on_gps_status(
                    self,
                    stype,
                    status
            ):

                print(
                    "GPS Status:",
                    stype,
                    status
                )

            def on_leave(self):

                try:

                    gps.stop()

                except Exception:

                    pass
class SafetyPinScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = WaveBackground()

        title = Label(
            text="[b]Safety PIN[/b]",
            markup=True,
            font_size=dp(30),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.10),
            pos_hint={"center_x": 0.5, "top": 0.90}
        )
        layout.add_widget(title)

        info = Label(
            text="Create a 4-digit PIN for your safety",
            font_size=dp(16),
            color=(0.80, 0.80, 0.88, 1),
            size_hint=(1, 0.08),
            pos_hint={"center_x": 0.5, "top": 0.80}
        )
        layout.add_widget(info)

        pin_input = TextInput(
            hint_text="Enter 4-digit PIN",
            password=True,
            input_filter="int",
            multiline=False,
            halign="center",
            font_size=dp(20),
            size_hint=(0.70, 0.08),
            pos_hint={"center_x": 0.5, "top": 0.68}
        )
        layout.add_widget(pin_input)

        confirm_input = TextInput(
            hint_text="Confirm 4-digit PIN",
            password=True,
            input_filter="int",
            multiline=False,
            halign="center",
            font_size=dp(20),
            size_hint=(0.70, 0.08),
            pos_hint={"center_x": 0.5, "top": 0.57}
        )
        layout.add_widget(confirm_input)

        message = Label(
            text="",
            font_size=dp(14),
            color=(1, 1, 1, 1),
            size_hint=(0.90, 0.08),
            pos_hint={"center_x": 0.5, "top": 0.48}
        )
        layout.add_widget(message)

        save_button = Button(
            text="Save PIN",
            font_size=dp(18),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.48, 0.30, 0.95, 1),
            size_hint=(0.65, 0.08),
            pos_hint={"center_x": 0.5, "center_y": 0.34}
        )
        layout.add_widget(save_button)

        back_button = Button(
            text="Back to Safety Dashboard",
            font_size=dp(15),
            color=(0.85, 0.85, 0.90, 1),
            background_normal="",
            background_color=(0, 0, 0, 0),
            size_hint=(0.75, 0.07),
            pos_hint={"center_x": 0.5, "center_y": 0.22}
        )
        layout.add_widget(back_button)

        def save_pin(instance):

            pin = pin_input.text
            confirm_pin = confirm_input.text

            if len(pin) != 4 or len(confirm_pin) != 4:
                message.text = "PIN must contain exactly 4 digits."

            elif pin != confirm_pin:
                message.text = "PINs do not match."

            else:
                app = App.get_running_app()

                app.config.set("Security", "pin", pin)
                app.config.write()

                message.text = "Safety PIN saved successfully."

                print("Safety PIN saved successfully")

        save_button.bind(on_release=save_pin)

        back_button.bind(
            on_release=lambda x: setattr(
                self.manager,
                "current",
                "dashboard"
            )
        )

        self.add_widget(layout)
class VerifyPinScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = WaveBackground()

        title = Label(
            text="[b]Verify Safety PIN[/b]",
            markup=True,
            font_size=dp(30),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.10),
            pos_hint={"center_x": 0.5, "top": 0.90}
        )
        layout.add_widget(title)

        info = Label(
            text="Enter your Safety PIN to continue",
            font_size=dp(16),
            color=(0.80, 0.80, 0.88, 1),
            size_hint=(1, 0.08),
            pos_hint={"center_x": 0.5, "top": 0.80}
        )
        layout.add_widget(info)

        pin_input = TextInput(
            hint_text="Enter 4-digit PIN",
            password=True,
            input_filter="int",
            multiline=False,
            halign="center",
            font_size=dp(20),
            size_hint=(0.70, 0.08),
            pos_hint={"center_x": 0.5, "top": 0.67}
        )

        pin_input.bind(
            size=lambda instance, value: setattr(
                instance,
                "text_size",
                (instance.width, instance.height)
            )
        )

        layout.add_widget(pin_input)

        message = Label(
            text="",
            font_size=dp(14),
            color=(1, 1, 1, 1),
            size_hint=(0.90, 0.08),
            pos_hint={"center_x": 0.5, "top": 0.55}
        )
        layout.add_widget(message)

        verify_button = Button(
            text="Verify PIN",
            font_size=dp(18),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.48, 0.30, 0.95, 1),
            size_hint=(0.65, 0.08),
            pos_hint={"center_x": 0.5, "center_y": 0.38}
        )
        layout.add_widget(verify_button)

        back_button = Button(
            text="Back to Safety Dashboard",
            font_size=dp(15),
            color=(0.85, 0.85, 0.90, 1),
            background_normal="",
            background_color=(0, 0, 0, 0),
            size_hint=(0.75, 0.07),
            pos_hint={"center_x": 0.5, "center_y": 0.25}
        )
        layout.add_widget(back_button)

        def verify_pin(instance):

            entered_pin = pin_input.text

            saved_pin = App.get_running_app().config.get(
                "Security",
                "pin"
            )

            if len(entered_pin) != 4:
                message.text = "Please enter your 4-digit PIN."

            elif entered_pin == saved_pin:
                message.text = "PIN verified successfully."
                print("PIN verified successfully")

            else:
                message.text = "Incorrect PIN."

        verify_button.bind(
            on_release=verify_pin
        )

        back_button.bind(
            on_release=lambda x: setattr(
                self.manager,
                "current",
                "dashboard"
            )
        )

        self.add_widget(layout)


class EmergencyContactsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_contacts_screen()

    def get_contacts(self):

        app = App.get_running_app()

        saved_contacts = app.config.get(
            "Contacts",
            "safe_contacts"
        )

        if not saved_contacts:
            return []

        try:
            contacts = json.loads(saved_contacts)

            if isinstance(contacts, list):
                return contacts

            return []

        except Exception:
            return []

    def save_contacts(self, contacts):

        app = App.get_running_app()

        app.config.set(
            "Contacts",
            "safe_contacts",
            json.dumps(contacts)
        )

        app.config.write()

    def build_contacts_screen(self):

        self.clear_widgets()

        layout = WaveBackground()

        # =========================
        # TITLE
        # =========================

        title = Label(
            text="[b]Emergency Contacts[/b]",
            markup=True,
            font_size=dp(29),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.10),
            pos_hint={
                "center_x": 0.5,
                "top": 0.94
            }
        )

        layout.add_widget(title)

        # =========================
        # INFO
        # =========================

        info = Label(
            text="Add up to 5 trusted Safe Contacts",
            font_size=dp(15),
            color=(0.80, 0.80, 0.88, 1),
            size_hint=(1, 0.06),
            pos_hint={
                "center_x": 0.5,
                "top": 0.86
            }
        )

        layout.add_widget(info)

        contacts = self.get_contacts()

        # =========================
        # CONTACT DISPLAY
        # =========================

        if not contacts:

            empty_label = Label(
                text=(
                    "[b]No Safe Contacts added yet.[/b]\n\n"
                    "Add trusted contacts who should receive "
                    "your emergency alerts."
                ),
                markup=True,
                font_size=dp(15),
                color=(1, 1, 1, 1),
                halign="center",
                valign="middle",
                size_hint=(0.88, 0.30),
                pos_hint={
                    "center_x": 0.5,
                    "top": 0.72
                }
            )

            empty_label.bind(
                size=lambda instance, value: setattr(
                    instance,
                    "text_size",
                    (instance.width, instance.height)
                )
            )

            layout.add_widget(empty_label)

        else:

            start_y = 0.75
            gap = 0.125

            for index, contact in enumerate(contacts):
                y_position = start_y - (index * gap)

                # =========================
                # CONTACT INFORMATION
                # =========================

                contact_label = Label(
                    text=(
                        f"[b]{index + 1}. "
                        f"{contact['name']}[/b]\n"
                        f"Phone: {contact['phone']}\n"
                        f"Relation: "
                        f"{contact.get('relation', 'Not specified')}"
                    ),
                    markup=True,
                    font_size=dp(13),
                    color=(1, 1, 1, 1),
                    halign="left",
                    valign="middle",
                    size_hint=(0.56, 0.105),
                    pos_hint={
                        "x": 0.07,
                        "top": y_position
                    }
                )

                contact_label.bind(
                    size=lambda instance, value: setattr(
                        instance,
                        "text_size",
                        (instance.width, instance.height)
                    )
                )

                layout.add_widget(contact_label)

                # =========================
                # EDIT BUTTON
                # =========================

                edit_button = Button(
                    text="Edit",
                    font_size=dp(13),
                    color=(1, 1, 1, 1),
                    background_normal="",
                    background_color=(0.48, 0.30, 0.95, 1),
                    size_hint=(0.14, 0.065),
                    pos_hint={
                        "x": 0.64,
                        "top": y_position - 0.015
                    }
                )

                layout.add_widget(edit_button)

                edit_button.bind(
                    on_release=lambda instance,
                                      i=index: self.open_edit_contact(i)
                )

                # =========================
                # DELETE BUTTON
                # =========================

                delete_button = Button(
                    text="Delete",
                    font_size=dp(12),
                    color=(1, 1, 1, 1),
                    background_normal="",
                    background_color=(0.70, 0.15, 0.25, 1),
                    size_hint=(0.16, 0.065),
                    pos_hint={
                        "x": 0.81,
                        "top": y_position - 0.015
                    }
                )

                layout.add_widget(delete_button)

                delete_button.bind(
                    on_release=lambda instance,
                                      i=index: self.delete_contact(i)
                )

        # =========================
        # ADD CONTACT BUTTON
        # =========================

        if len(contacts) < 5:

            add_button = Button(
                text="Add Safe Contact",
                font_size=dp(17),
                color=(1, 1, 1, 1),
                background_normal="",
                background_color=(0.48, 0.30, 0.95, 1),
                size_hint=(0.70, 0.08),
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.18
                }
            )

            layout.add_widget(add_button)

            add_button.bind(
                on_release=lambda instance:
                self.open_add_contact()
            )

        else:

            limit_label = Label(
                text="Maximum of 5 Safe Contacts reached.",
                font_size=dp(14),
                color=(0.90, 0.90, 0.95, 1),
                size_hint=(0.90, 0.06),
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.18
                }
            )

            layout.add_widget(limit_label)

        # =========================
        # BACK BUTTON
        # =========================

        back_button = Button(
            text="Back to Safety Dashboard",
            font_size=dp(15),
            color=(0.85, 0.85, 0.90, 1),
            background_normal="",
            background_color=(0, 0, 0, 0),
            size_hint=(0.80, 0.07),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.08
            }
        )

        layout.add_widget(back_button)

        back_button.bind(
            on_release=lambda instance:
            setattr(
                self.manager,
                "current",
                "dashboard"
            )
        )

        self.add_widget(layout)

    # =========================
    # ADD CONTACT
    # =========================

    def open_add_contact(self):

        self.show_contact_form(
            mode="add",
            contact_index=None
        )

    # =========================
    # EDIT CONTACT
    # =========================

    def open_edit_contact(self, index):

        self.show_contact_form(
            mode="edit",
            contact_index=index
        )

    # =========================
    # DELETE CONTACT
    # =========================

    def delete_contact(self, index):

        contacts = self.get_contacts()

        if index < len(contacts):
            deleted_name = contacts[index]["name"]

            contacts.pop(index)

            self.save_contacts(contacts)

            print(
                f"Safe Contact deleted: {deleted_name}"
            )

            self.build_contacts_screen()

    # =========================
    # CONTACT FORM
    # =========================

    def show_contact_form(
            self,
            mode,
            contact_index
    ):

        self.clear_widgets()

        layout = WaveBackground()

        # =========================
        # TITLE
        # =========================

        if mode == "add":

            title_text = "Add Safe Contact"

        else:

            title_text = "Edit Safe Contact"

        title = Label(
            text=f"[b]{title_text}[/b]",
            markup=True,
            font_size=dp(29),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.10),
            pos_hint={
                "center_x": 0.5,
                "top": 0.91
            }
        )

        layout.add_widget(title)

        # =========================
        # NAME
        # =========================

        name_input = TextInput(
            hint_text="Contact Name",
            multiline=False,
            font_size=dp(17),
            size_hint=(0.80, 0.075),
            pos_hint={
                "center_x": 0.5,
                "top": 0.75
            },
            background_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)]
        )

        layout.add_widget(name_input)

        # =========================
        # PHONE
        # =========================

        phone_input = TextInput(
            hint_text="Phone Number",
            multiline=False,
            font_size=dp(17),
            size_hint=(0.80, 0.075),
            pos_hint={
                "center_x": 0.5,
                "top": 0.63
            },
            background_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)]
        )

        layout.add_widget(phone_input)

        # =========================
        # RELATIONSHIP
        # OPTIONAL
        # =========================

        relation_input = TextInput(
            hint_text="Relationship (Optional)",
            multiline=False,
            font_size=dp(16),
            size_hint=(0.80, 0.075),
            pos_hint={
                "center_x": 0.5,
                "top": 0.51
            },
            background_color=(1, 1, 1, 1),
            padding=[dp(15), dp(12)]
        )

        layout.add_widget(relation_input)

        # =========================
        # MESSAGE
        # =========================

        message = Label(
            text="",
            font_size=dp(14),
            color=(1, 1, 1, 1),
            size_hint=(0.90, 0.08),
            pos_hint={
                "center_x": 0.5,
                "top": 0.42
            }
        )

        layout.add_widget(message)

        # =========================
        # LOAD EXISTING CONTACT
        # =========================

        contacts = self.get_contacts()

        if (
                mode == "edit"
                and contact_index is not None
                and contact_index < len(contacts)
        ):
            existing = contacts[contact_index]

            name_input.text = existing.get(
                "name",
                ""
            )

            phone_input.text = existing.get(
                "phone",
                ""
            )

            relation_input.text = existing.get(
                "relation",
                ""
            )

        # =========================
        # SAVE BUTTON
        # =========================

        save_button = Button(
            text="Save Contact",
            font_size=dp(18),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.48, 0.30, 0.95, 1),
            size_hint=(0.65, 0.08),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.31
            }
        )

        layout.add_widget(save_button)

        # =========================
        # CANCEL BUTTON
        # =========================

        cancel_button = Button(
            text="Cancel",
            font_size=dp(15),
            color=(0.85, 0.85, 0.90, 1),
            background_normal="",
            background_color=(0, 0, 0, 0),
            size_hint=(0.60, 0.07),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.20
            }
        )

        layout.add_widget(cancel_button)

        # =========================
        # SAVE ACTION
        # =========================

        def save_action(instance):

            name = name_input.text.strip()
            phone = phone_input.text.strip()
            relation = relation_input.text.strip()

            # Name required

            if name == "":
                message.text = (
                    "Please enter the contact name."
                )

                return

            # Phone required

            if phone == "":
                message.text = (
                    "Please enter the phone number."
                )

                return

            # Basic phone validation

            phone_digits = "".join(
                character
                for character in phone
                if character.isdigit()
            )

            if len(phone_digits) < 7:
                message.text = (
                    "Please enter a valid phone number."
                )

                return

            # Relationship optional

            if relation == "":
                relation = "Not specified"

            contact = {
                "name": name,
                "phone": phone,
                "relation": relation
            }

            # =========================
            # ADD
            # =========================

            if mode == "add":

                contacts = self.get_contacts()

                if len(contacts) >= 5:
                    message.text = (
                        "Maximum of 5 Safe Contacts reached."
                    )

                    return

                contacts.append(contact)

            # =========================
            # EDIT
            # =========================

            else:

                contacts = self.get_contacts()

                if (
                        contact_index is None
                        or contact_index >= len(contacts)
                ):
                    message.text = (
                        "Contact could not be updated."
                    )

                    return

                contacts[contact_index] = contact

            # =========================
            # SAVE
            # =========================

            self.save_contacts(contacts)

            print(
                "Safe Contact saved successfully"
            )

            self.build_contacts_screen()

        save_button.bind(
            on_release=save_action
        )

        # =========================
        # CANCEL
        # =========================

        cancel_button.bind(
            on_release=lambda instance:
            self.build_contacts_screen()
        )

        self.add_widget(layout)
class IncidentTimelineScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        self.build_timeline_screen()

    def build_timeline_screen(self):

        self.clear_widgets()

        layout = WaveBackground()

        title = Label(
            text="[b]Incident Timeline[/b]",
            markup=True,
            font_size=dp(29),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.10),
            pos_hint={
                "center_x": 0.5,
                "top": 0.95
            }
        )

        layout.add_widget(title)

        app = App.get_running_app()
        incidents = app.get_emergency_events()

        if not incidents:

            empty_label = Label(
                text=(
                    "[b]No emergency incidents recorded.[/b]\n\n"
                    "Your emergency events will appear here."
                ),
                markup=True,
                font_size=dp(16),
                color=(1, 1, 1, 1),
                halign="center",
                valign="middle",
                size_hint=(0.88, 0.30),
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.55
                }
            )

            empty_label.bind(
                size=lambda instance, value: setattr(
                    instance,
                    "text_size",
                    (instance.width, instance.height)
                )
            )

            layout.add_widget(empty_label)

        else:

            scroll_view = ScrollView(
                size_hint=(0.94, 0.72),
                pos_hint={
                    "center_x": 0.5,
                    "top": 0.84
                },
                do_scroll_x=False,
                do_scroll_y=True
            )

            timeline_layout = FloatLayout(
                size_hint_y=None
            )

            reversed_incidents = list(
                reversed(incidents)
            )

            incident_height = dp(145)

            timeline_layout.height = (
                len(reversed_incidents) *
                incident_height
            )

            y_position = (
                timeline_layout.height -
                incident_height
            )

            for incident in reversed_incidents:

                timestamp = incident.get(
                    "timestamp",
                    "Unknown time"
                )

                event_type = incident.get(
                    "type",
                    "Emergency Event"
                )

                status = incident.get(
                    "status",
                    "Unknown"
                )

                latitude = incident.get(
                    "latitude"
                )

                longitude = incident.get(
                    "longitude"
                )

                acknowledged = incident.get(
                    "acknowledged",
                    False
                )

                if latitude is not None and longitude is not None:
                    location_text = (
                        f"Location: {latitude}, {longitude}"
                    )
                else:
                    location_text = (
                        "Location: Not available"
                    )

                if acknowledged:
                    review_text = "Review: Acknowledged"
                else:
                    review_text = "Review: Not Acknowledged"

                incident_label = Label(
                    text=(
                        f"[b]🚨 {event_type}[/b]\n"
                        f"Date & Time: {timestamp}\n"
                        f"Status: {status}\n"
                        f"{location_text}\n"
                        f"{review_text}"
                    ),
                    markup=True,
                    font_size=dp(14),
                    color=(1, 1, 1, 1),
                    halign="left",
                    valign="middle",
                    size_hint=(
                        0.90,
                        None
                    ),
                    height=incident_height,
                    pos_hint={
                        "center_x": 0.5
                    },
                    y=y_position
                )

                incident_label.bind(
                    size=lambda instance, value:
                    setattr(
                        instance,
                        "text_size",
                        (
                            instance.width,
                            instance.height
                        )
                    )
                )

                timeline_layout.add_widget(
                    incident_label
                )

                y_position -= incident_height

            scroll_view.add_widget(
                timeline_layout
            )

            layout.add_widget(
                scroll_view
            )

            acknowledge_button = Button(
                text="Acknowledge Latest Incident",
                font_size=dp(15),
                color=(1, 1, 1, 1),
                background_normal="",
                background_color=(
                    0.48,
                    0.30,
                    0.95,
                    1
                ),
                size_hint=(0.72, 0.07),
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.12
                }
            )

            layout.add_widget(
                acknowledge_button
            )

            acknowledge_button.bind(
                on_release=lambda instance:
                self.acknowledge_latest_incident()
            )

        back_button = Button(
            text="Back to Safety Dashboard",
            font_size=dp(15),
            color=(0.85, 0.85, 0.90, 1),
            background_normal="",
            background_color=(0, 0, 0, 0),
            size_hint=(0.80, 0.06),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.045
            }
        )

        layout.add_widget(
            back_button
        )

        back_button.bind(
            on_release=lambda instance:
            setattr(
                self.manager,
                "current",
                "dashboard"
            )
        )

        self.add_widget(layout)

    def acknowledge_latest_incident(self):

        app = App.get_running_app()

        incidents = app.get_emergency_events()

        if not incidents:
            return

        incidents[-1]["acknowledged"] = True

        incidents[-1]["acknowledged_at"] = (
            datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        app.config.set(
            "Emergency",
            "incident_log",
            json.dumps(incidents)
        )

        app.config.write()

        print(
            "Latest emergency incident acknowledged."
        )

        self.build_timeline_screen()
class SafetyTimerScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer_event = None
        self.remaining_seconds = 10

        self.build_timer_screen()

    def build_timer_screen(self):

        self.clear_widgets()

        layout = WaveBackground()

        title = Label(
            text="[b]Safety Verification[/b]",
            markup=True,
            font_size=dp(30),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.10),
            pos_hint={
                "center_x": 0.5,
                "top": 0.91
            }
        )

        layout.add_widget(title)

        info = Label(
            text="Please confirm your safety",
            font_size=dp(17),
            color=(0.80, 0.80, 0.88, 1),
            size_hint=(1, 0.08),
            pos_hint={
                "center_x": 0.5,
                "top": 0.80
            }
        )

        layout.add_widget(info)

        self.timer_label = Label(
            text="10",
            font_size=dp(70),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.20),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.60
            }
        )

        layout.add_widget(self.timer_label)

        self.status_label = Label(
            text="10 seconds remaining",
            font_size=dp(16),
            color=(0.85, 0.85, 0.90, 1),
            size_hint=(1, 0.07),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.47
            }
        )

        layout.add_widget(self.status_label)

        start_button = Button(
            text="Start 10-Second Timer",
            font_size=dp(18),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.48, 0.30, 0.95, 1),
            size_hint=(0.70, 0.085),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.32
            }
        )

        layout.add_widget(start_button)

        start_button.bind(
            on_release=self.start_timer
        )

        cancel_button = Button(
            text="Cancel",
            font_size=dp(16),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.70, 0.15, 0.25, 1),
            size_hint=(0.55, 0.075),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.21
            }
        )

        layout.add_widget(cancel_button)

        cancel_button.bind(
            on_release=self.cancel_timer
        )

        back_button = Button(
            text="Back to Safety Dashboard",
            font_size=dp(15),
            color=(0.85, 0.85, 0.90, 1),
            background_normal="",
            background_color=(0, 0, 0, 0),
            size_hint=(0.80, 0.07),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.08
            }
        )

        layout.add_widget(back_button)

        back_button.bind(
            on_release=self.go_back
        )

        self.add_widget(layout)

    def start_timer(self, instance):

        if self.timer_event is not None:
            return

        self.remaining_seconds = 10

        self.timer_label.text = "10"

        self.status_label.text = (
            "10 seconds remaining"
        )

        self.timer_event = Clock.schedule_interval(
            self.update_timer,
            1
        )

    def update_timer(self, dt):

        if self.remaining_seconds > 0:

            self.remaining_seconds -= 1

            self.timer_label.text = str(
                self.remaining_seconds
            )

            self.status_label.text = (
                f"{self.remaining_seconds} "
                f"seconds remaining"
            )

        else:

            self.finish_timer()

    def finish_timer(self):

        if self.timer_event is not None:

            self.timer_event.cancel()
            self.timer_event = None

        self.timer_label.text = "0"

        self.status_label.text = (
            "Safety verification time ended."
        )

        print(
            "Safety verification timer finished."
        )

    def cancel_timer(self, instance):

        if self.timer_event is not None:

            self.timer_event.cancel()
            self.timer_event = None

        self.remaining_seconds = 10

        self.timer_label.text = "10"

        self.status_label.text = (
            "Safety verification cancelled."
        )

    def go_back(self, instance):

        if self.timer_event is not None:

            self.timer_event.cancel()
            self.timer_event = None

        self.remaining_seconds = 10

        self.manager.current = "dashboard"
class SOSVerificationScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer_event = None
        self.remaining_seconds = 10
        self.latitude = None
        self.longitude = None

        self.build_sos_screen()

    def on_enter(self):

        # Screen open hote hi fresh 10-second countdown start hoga
        self.remaining_seconds = 10
        self.timer_label.text = "10"
        self.status_label.text = (
            "SOS will activate when the timer reaches 0."
        )

        # Thori si delay taake screen pehle properly show ho
        Clock.schedule_once(
            lambda dt: self.start_countdown(),
            0.2
        )

    def build_sos_screen(self):

        self.clear_widgets()

        layout = WaveBackground()

        title = Label(
            text="[b]Emergency SOS[/b]",
            markup=True,
            font_size=dp(30),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.10),
            pos_hint={
                "center_x": 0.5,
                "top": 0.91
            }
        )
        layout.add_widget(title)

        warning = Label(
            text=(
                "[b]Emergency verification started[/b]\n"
                "If you are safe, cancel the SOS."
            ),
            markup=True,
            font_size=dp(16),
            color=(1, 0.85, 0.85, 1),
            halign="center",
            valign="middle",
            size_hint=(0.88, 0.14),
            pos_hint={
                "center_x": 0.5,
                "top": 0.80
            }
        )

        warning.bind(
            size=lambda instance, value: setattr(
                instance,
                "text_size",
                (instance.width, instance.height)
            )
        )

        layout.add_widget(warning)

        self.timer_label = Label(
            text="10",
            font_size=dp(70),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.20),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.59
            }
        )

        layout.add_widget(self.timer_label)

        self.status_label = Label(
            text="SOS will activate when the timer reaches 0.",
            font_size=dp(15),
            color=(0.85, 0.85, 0.90, 1),
            halign="center",
            valign="middle",
            size_hint=(0.90, 0.09),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.46
            }
        )

        self.status_label.bind(
            size=lambda instance, value: setattr(
                instance,
                "text_size",
                (instance.width, instance.height)
            )
        )

        layout.add_widget(self.status_label)

        confirm_button = Button(
            text="Activate SOS Now",
            font_size=dp(18),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.85, 0.12, 0.25, 1),
            size_hint=(0.70, 0.085),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.31
            }
        )

        layout.add_widget(confirm_button)

        confirm_button.bind(
            on_release=self.activate_sos
        )

        cancel_button = Button(
            text="I'm Safe - Cancel SOS",
            font_size=dp(16),
            color=(1, 1, 1, 1),
            background_normal="",
            background_color=(0.18, 0.16, 0.28, 1),
            size_hint=(0.70, 0.075),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.20
            }
        )

        layout.add_widget(cancel_button)

        cancel_button.bind(
            on_release=self.cancel_sos
        )

        self.add_widget(layout)

    def start_countdown(self):

        if self.timer_event is not None:
            self.timer_event.cancel()

        self.remaining_seconds = 10

        self.timer_label.text = "10"

        self.status_label.text = (
            "SOS will activate when the timer reaches 0."
        )

        self.timer_event = Clock.schedule_interval(
            self.update_countdown,
            1
        )

    def update_countdown(self, dt):

        if self.remaining_seconds > 1:

            self.remaining_seconds -= 1

            self.timer_label.text = str(
                self.remaining_seconds
            )

            self.status_label.text = (
                f"SOS will activate in "
                f"{self.remaining_seconds} seconds."
            )

        else:

            self.remaining_seconds = 0

            self.timer_label.text = "0"

            self.status_label.text = (
                "Emergency SOS activating..."
            )

            self.activate_sos(None)

    def activate_sos(self, instance):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        self.timer_label.text = "SOS ACTIVATED"
        self.status_label.text = "Emergency SOS has been activated."

        app = App.get_running_app()

        location_screen = self.manager.get_screen("location")

        latitude = location_screen.latitude
        longitude = location_screen.longitude

        contacts_screen = self.manager.get_screen("emergency_contacts")
        contacts = contacts_screen.get_contacts()

        emergency_event = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Emergency SOS",
            "status": "Activated",
            "latitude": latitude,
            "longitude": longitude,
            "contacts_count": len(contacts)
        }

        app.save_emergency_event(emergency_event)
        app.send_emergency_alerts(emergency_event, contacts)

        print("EMERGENCY SOS ACTIVATED")
        print("Emergency event:", emergency_event)

        if latitude is not None and longitude is not None:
            print("Location:", latitude, longitude)
        else:
            print("Location not available yet.")

        print("Safe contacts:", len(contacts))

    def cancel_sos(self, instance):

        if self.timer_event is not None:
            self.timer_event.cancel()
            self.timer_event = None

        self.remaining_seconds = 10

        self.manager.current = "dashboard"

class OfflineVoiceDetector:
    def __init__(self, on_help_detected):
                self.on_help_detected = on_help_detected
                self.running = False
                self.thread = None

                self.model_path = os.path.join(
                    os.path.dirname(__file__),
                    "vosk-model",
                    "vosk-model-small-en-us-0.15"
                )

    def start(self):
                if self.running:
                    return

                self.running = True
                self.thread = threading.Thread(
                    target=self._listen,
                    daemon=True
                )
                self.thread.start()

    def stop(self):
                self.running = False

    def _listen(self):
                try:
                    print("Loading offline Vosk model...")

                    model = vosk.Model(self.model_path)

                    print("VOSK MODEL LOADED")
                    print("OFFLINE VOICE DETECTION READY")

                    # Microphone code will be connected in the next step.

                except Exception as e:
                    print("Offline voice detection error:", e)
class SafeHerApp(App):
    def load_voice_model(self):
        model_path = os.path.join(
            os.path.dirname(__file__),
            "vosk-model",
            "vosk-model-small-en-us-0.15"
        )

        print("Loading Vosk model from:", model_path)

        self.voice_model = Model(model_path)

        print("VOSK MODEL LOADED SUCCESSFULLY")
    def build_config(self, config):
        config.setdefaults("Security", {"pin": ""})
        config.setdefaults("Contacts", {"safe_contacts": "[]"})
        config.setdefaults("Emergency", {"incident_log": "[]"})
        config.setdefaults("User", {"full_name": ""})
    def build_alert_message(self, event):

        user_name = self.config.get(
            "User",
            "full_name"
        ).strip()

        if not user_name:
            user_name = "SafeHER User"

        message = (
            "🚨 SAFEHER EMERGENCY ALERT 🚨\n\n"
            "EMERGENCY SOS ACTIVATED\n\n"
            f"Person: {user_name}\n"
            f"Time: {event['timestamp']}\n"
        )

        latitude = event.get("latitude")
        longitude = event.get("longitude")

        if latitude is not None and longitude is not None:

            message += (
                f"Location: {latitude}, {longitude}\n"
                f"Map: https://maps.google.com/?q={latitude},{longitude}\n"
            )

        else:

            message += (
                "Location: Not available\n"
            )

        message += (
            "\nPlease check on this person immediately.\n\n"
            "This is an emergency alert from SafeHER."
        )

        return message

    def send_sms_alert(self, phone, message):
            if platform.system() == "Android":
                try:
                    from plyer import sms

                    sms.send(
                        recipient=phone,
                        message=message
                    )

                    print("SMS sent to:", phone)

                except Exception as e:
                    print("SMS error:", e)

            else:
                print("\n--- SMS PREVIEW ---")
                print("To:", phone)
                print(message)
                print("-------------------\n")
    def make_emergency_call(self, phone):
        if platform.system() == "Android":
            try:
                from jnius import autoclass

                Intent = autoclass("android.content.Intent")
                Uri = autoclass("android.net.Uri")
                PythonActivity = autoclass(
                    "org.kivy.android.PythonActivity"
                )

                intent = Intent(Intent.ACTION_CALL)
                intent.setData(
                    Uri.parse("tel:" + phone)
                )

                current_activity = PythonActivity.mActivity
                current_activity.startActivity(intent)

                print("Emergency call started:", phone)

            except Exception as e:
                print("Call error:", e)

        else:
            print("\n--- CALL PREVIEW ---")
            print("Emergency call would be made to:", phone)
            print("--------------------\n")
    def send_emergency_alerts(self, event, contacts):
            message = self.build_alert_message(event)

            print("\n==============================")
            print("SAFEHER EMERGENCY ALERT SYSTEM")
            print("==============================")

            for contact in contacts:
                phone = contact.get("phone")

                if not phone:
                    continue

                print("Alerting:", contact.get("name", "Unknown"))

                self.send_sms_alert(phone, message)
                self.make_emergency_call(phone)

            print("==============================\n")

    def handle_offline_emergency(self, event, contacts):
        print("\n==============================")
        print("OFFLINE EMERGENCY HANDLER")
        print("==============================")

        message = self.build_alert_message(event)

        if not contacts:
            print("No emergency contacts saved.")
            print("Emergency event remains saved locally.")
            return

        print("Internet communication unavailable.")
        print("Using emergency fallback: SMS + CALL")

        for contact in contacts:
            phone = contact.get("phone")

            if not phone:
                continue

            print("Offline fallback alerting:", contact.get("name", "Unknown"))

            self.send_sms_alert(phone, message)
            self.make_emergency_call(phone)

        print("==============================\n")

    def save_emergency_event(self, event):
            try:
                current_log = self.config.get("Emergency", "incident_log")
                incidents = json.loads(current_log)

                incidents.append(event)

                self.config.set(
                    "Emergency",
                    "incident_log",
                    json.dumps(incidents)
                )
                self.config.write()

                print("Emergency event saved successfully.")

            except Exception as e:
                print("Error saving emergency event:", e)

    def get_emergency_events(self):
            try:
                current_log = self.config.get("Emergency", "incident_log")
                return json.loads(current_log)

            except Exception as e:
                print("Error reading emergency events:", e)
                return []
    def build(self):
        manager = ScreenManager()

        # =========================
        # HOME SCREEN
        # =========================

        home_screen = Screen(name="home")
        home_layout = WaveBackground()

        logo_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "safeherlogo.png"
        )

        logo = Image(
            source=logo_path,
            size_hint=(0.55, 0.30),
            pos_hint={"center_x": 0.5, "top": 0.88},
            allow_stretch=True,
            keep_ratio=True
        )

        home_layout.add_widget(logo)

        title = Label(
            text="[b]Safe[/b][color=#8B5CF6][b]Her[/b][/color]",
            markup=True,
            font_size=dp(45),
            size_hint=(1, 0.10),
            pos_hint={"center_x": 0.5, "top": 0.55}
        )

        home_layout.add_widget(title)

        tagline = Label(
            text="Stay strong, stay safe.",
            font_size=dp(20),
            color=(0.90, 0.90, 0.95, 1),
            size_hint=(1, 0.08),
            pos_hint={"center_x": 0.5, "top": 0.47}
        )

        home_layout.add_widget(tagline)

        button = Button(
            text="Get Started",
            font_size=dp(20),
            color=(1, 1, 1, 1),
            size_hint=(0.72, 0.085),
            pos_hint={"center_x": 0.5, "y": 0.13},
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0)
        )

        with button.canvas.before:
            Color(0.48, 0.30, 0.95, 1)

            button_bg = RoundedRectangle(
                pos=button.pos,
                size=button.size,
                radius=[dp(35)]
            )

        def update_button(*args):
            button_bg.pos = button.pos
            button_bg.size = button.size

        button.bind(
            pos=update_button,
            size=update_button
        )

        home_layout.add_widget(button)

        button.bind(
            on_release=lambda x: setattr(
                manager,
                "current",
                "create_account"
            )
        )

        # =========================
        # ADD ALL SCREENS
        # =========================

        manager.add_widget(home_screen)

        manager.add_widget(
            LoginScreen(name="login")
        )

        manager.add_widget(
            CreateAccountScreen(name="create_account")
        )

        manager.add_widget(
            DashboardScreen(name="dashboard")
        )

        manager.add_widget(
            SafetyPinScreen(name="safety_pin")
        )
        manager.add_widget(
            VerifyPinScreen(name="verify_pin")
        )
        manager.add_widget(
            EmergencyContactsScreen(name="emergency_contacts")
        )
        manager.add_widget(
            SafetyTimerScreen(name="safety_timer")
        )
        manager.add_widget(
            SOSVerificationScreen(name="sos_verification")
        )
        manager.add_widget(
            LocationScreen(name="location")
        )
        manager.add_widget(
            IncidentTimelineScreen(name="incident_timeline")
        )
        # Add Home layout
        home_screen.add_widget(home_layout)

        # Start from Home
        manager.current = "home"

        return manager
    def on_start(self):

        print("APP STARTED - STARTING OFFLINE VOICE DETECTION")

        try:
            self.load_voice_model()

            self.voice_listener_running = True

            self.voice_thread = threading.Thread(
                target=self.voice_listener,
                daemon=True
            )

            self.voice_thread.start()

        except Exception as error:
            print("Offline voice detection error:", error)
    def voice_listener(self):

        try:

            audio = pyaudio.PyAudio()

            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000
            )

            stream.start_stream()

            recognizer = KaldiRecognizer(
                self.voice_model,
                16000
            )

            print("Offline Voice Detection: Listening for HELP...")

            while self.voice_listener_running:

                data = stream.read(
                    4000,
                    exception_on_overflow=False
                )

                if recognizer.AcceptWaveform(data):

                    result = json.loads(
                        recognizer.Result()
                    )

                    detected_text = result.get(
                        "text",
                        ""
                    ).lower().strip()

                    if detected_text:

                        print(
                            "Voice recognized:",
                            detected_text
                        )

                    if "help" in detected_text:

                        Clock.schedule_once(
                            self.trigger_voice_sos,
                            0
                        )

            stream.stop_stream()
            stream.close()
            audio.terminate()

        except Exception as error:

            print(
                "Offline voice detection error:",
                error
            )

    def trigger_voice_sos(self, dt):

        print("VOICE TRIGGER DETECTED: HELP")

        if self.root.current == "dashboard":
            self.root.current = "sos_verification"
    def on_stop(self):

        self.voice_listener_running = False
if __name__ == "__main__":
    SafeHerApp().run()