default persistent.lovense_local_ip = ""
default persistent.lovense_http_port = ""


screen connect_lovense():
    tag lovense
    predict False

    default image_path = "lovense/images/"
    default qr_image = None

    add image_path + "background.webp"

    imagebutton:
        idle "return_button_idle"
        hover "return_button_hover"
        action Hide()

    text "Connect to Lovense App" xalign 0.5 ypos 50 style "montserrat_extra_bold_64"

    hbox:
        align (0.5, 1.0)
        spacing 100

        # Game Mode
        vbox:
            align (0.5, 1.0)
            yoffset -200
            spacing 10

            add "lovense/images/game_mode_example.webp" xalign 0.5

            null height 30

            button:
                idle_background "blue_button_idle"
                hover_background "blue_button_hover"
                action ui.callsinnewcontext("lovense_connect_via_game_mode")
                padding (40, 25)
                align (0.5, 0.5)

                text "Connect With Game Mode" align (0.5, 0.5)

            text "No connection to external servers (LAN Only)" align (0.5, 0.5)

        # QR Code
        if persistent.lovense_http_port != "Server Offline":
            vbox:
                align (0.5, 1.0)
                yoffset -200
                spacing 10

                if qr_image is not None:
                    add qr_image xalign 0.5

                null height 30

                button:
                    idle_background "blue_button_idle"
                    hover_background "blue_button_hover"
                    action ui.callsinnewcontext("lovense_connect_via_qr_code")
                    padding (40, 25)
                    xalign 0.5

                    text "Connect With QR Code" align (0.5, 0.5)

                text "Requires connection to Lovense Server"

    vbox:
        align (0.5, 1.0)
        yoffset -50
        spacing 10

        text "Local IP: {}".format(persistent.lovense_local_ip)
        text "HTTP Port: {}".format(persistent.lovense_http_port)

    textbutton "Get your Lovense toys here":
        action OpenURL("https://www.lovense.com/r/mw4xb8")
        align (1.0, 1.0)
        offset (-50, -50)
        text_size 32

    timer 5 action Function(set_lovense_user) repeat True
    on "show" action SetScreenVariable("qr_image", download_qr_code())


image lovense_remote_download = "lovense/images/lovense_remote_download.webp"
image lovense_remote_profile = "lovense/images/lovense_remote_profile.webp"
image lovense_remote_game_mode = "lovense/images/lovense_remote_game_mode.webp"
image lovense_input_local_ip = "lovense/images/input_local_ip.webp"
image lovense_input_http_port = "lovense/images/input_http_port.webp"

image lovense_plus_view = "lovense/images/lovense_remote_plus_button.webp"
image lovense_scan_qr = "lovense/images/lovense_remote_scan_qr.webp"


label lovense_connect_via_game_mode:
    show black

    show lovense_remote_download
    "1. Download the Lovense Remote App (Compatibile: iOS, Android and Desktop)"
    hide lovense_remote_download

    show lovense_remote_profile
    "2. Head to the \"Me\" view"
    hide lovense_remote_profile

    show lovense_remote_game_mode
    "3. Select \"Settings\" and turn on \"Game Mode\""
    hide lovense_remote_game_mode

    show lovense_input_local_ip
    $ persistent.lovense_local_ip = renpy.input("4. Enter Local IP", allow="0123456789.")
    hide lovense_input_local_ip

    show lovense_input_http_port
    $ persistent.lovense_http_port = renpy.input("5. Enter HTTP Port", allow="0123456789.")
    hide lovense_input_http_port

    return

label lovense_connect_via_qr_code:
    show black

    show lovense_remote_download
    "1. Download the Lovense Remote App (Compatibile: iOS, Android and Desktop)"
    hide lovense_remote_download

    show lovense_plus_view
    "2. Click on the \"+\" icon"
    hide lovense_plus_view

    show lovense_scan_qr
    "3. Select \"Scan QR\""
    hide lovense_scan_qr

    $ download_qr_code()

    show expression "lovense_qr_code.jpg" at truecenter
    "4. Scan the above QR code to connect"
    hide expression "lovense_qr_code.jpg" at truecenter

    return