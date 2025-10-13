init offset = -1











style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb_offset 0
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)





















screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"




    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0



init python:
    config.character_id_prefixes.append('namebox')


style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    line_spacing -5












screen input(prompt):
    style_prefix "input"

    window:

        has vbox
        xalign gui.dialogue_text_xalign
        xpos gui.dialogue_xpos
        xsize gui.dialogue_width
        ypos gui.dialogue_ypos

        text prompt style "input_prompt"
        input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width










screen choice(items):
    style_prefix "choice"
    add Image("gui/choice_window.png")
    vbox:
        for i in items:
            textbutton i.caption action [Play("sfx","audio/PhoneSelect.mp3"),i.action]




define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.47
    yalign 0.3
    yanchor 0.0
    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")






screen quick_menu():


    zorder 100

    if quick_menu:

        vbox:
            style_prefix "quick"
            spacing -5

        imagebutton:
            idle "gui/back_pills_vert.png"
            action Function(renpy.rollback, force=False, checkpoints=1, defer=False, greedy=True, label=None, abnormal=False)
            xalign 0.086
            yalign 0.995

        imagebutton:
            idle "gui/pause_phone.png"
            action ShowMenu()
            xalign 0.964
            yalign 0.979








init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button:
    xalign 1.0

style quick_button_text is button_text

style quick_button_text:
    xalign 1.0
    size 50
    color '#000000'
    hover_color '#555555'
    insensitive_color 'FF0000'












screen navigation():


    style_prefix "navigation"

    imagebutton:
        idle "NEWGAME.png"
        hover "NEWGAME_selected.png"
        xpos 0
        ypos 0
        focus_mask "NEWGAME_mask.png"
        activate_sound "audio/MainMenuPress.mp3"
        hover_sound "audio/MainMenuRollover.mp3"
        action SetField(persistent, "new_ending", False), Start()

    imagebutton:
        idle "CONTINUE.png"
        hover "CONTINUE_selected.png"
        xpos 0
        ypos 0
        focus_mask "CONTINUE_mask.png"
        activate_sound "audio/MainMenuPress.mp3"
        hover_sound "audio/MainMenuRollover.mp3"
        action SetField(persistent, "new_ending", False), ShowMenu("load")

    imagebutton:
        idle "OPTIONS.png"
        hover "OPTIONS_selected.png"
        xpos 0
        ypos 0
        focus_mask "OPTIONS_mask.png"
        activate_sound "audio/MainMenuPress.mp3"
        hover_sound "audio/MainMenuRollover.mp3"
        action SetField(persistent, "new_ending", False), ShowMenu("preferences")


    imagebutton:
        idle "ABOUT.png"
        hover "ABOUT_selected.png"
        xpos 0
        ypos 0
        focus_mask "ABOUT_mask.png"
        activate_sound "audio/MainMenuPress.mp3"
        hover_sound "audio/MainMenuRollover.mp3"
        action SetField(persistent, "new_ending", False), ShowMenu("about")

    imagebutton:
        idle "EXIT.png"
        hover "EXIT_selected.png"
        xpos 0
        ypos 0
        focus_mask "EXIT_mask.png"
        activate_sound "audio/MainMenuPress.mp3"
        hover_sound "audio/MainMenuRollover.mp3"
        action SetField(persistent, "new_ending", False), Quit()





style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")

transform main_logo_transform:
    xalign .7 yalign 0.3 size (580.0*1.2,395.0*1.2) xanchor .5 yanchor .5
    block:
        easein 0.35 size (580.0*1.3, 395.0*1.3)
        linear 1.5 size (580.0*1.2,395.0*1.2)
        repeat







screen main_menu():
    tag menu



    style_prefix "main_menu"

    add gui.main_menu_background


    frame


    if persistent.endings:
        imagebutton:
            idle "gui/ending_tracker/text_access.png"
            hover "gui/ending_tracker/text_access.png"

            action Show("ending_tracker_screen"), With(None), Play("sound", "audio/Phone_slide.mp3"), SetField(persistent, "new_ending", False)
            xalign 0.925
            yalign 0.9

            at idle_rotate



    use navigation

    if gui.show_name:
        add Image("gui/ClassOf09logo.png") at main_logo_transform

    if persistent.new_ending:
        on "show":
            action Play("sound", "audio/NewTextAlert.mp3")
        add "new_message_animation"

transform idle_rotate:
    rotate 0
    linear 1.0 rotate 3
    linear 1.0 rotate 0
    linear 1.0 rotate 3
    linear 1.0 rotate 0
    repeat

image new_message_animation:
    "NewMessageSequence/NewMessage_0001.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0002.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0003.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0004.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0005.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0006.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0007.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0008.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0009.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0010.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0011.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0012.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0013.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0014.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0015.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0016.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0017.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0018.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0019.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0020.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0021.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0022.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0023.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0024.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0025.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0026.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0027.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0028.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0029.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0030.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0031.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0032.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0033.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0034.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0035.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0036.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0037.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0038.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0039.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0040.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0041.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0042.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0043.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0044.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0045.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0046.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0047.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0048.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0049.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0050.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0051.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0052.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0053.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0054.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0055.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0056.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0057.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0058.png"
    pause 0.041
    "NewMessageSequence/NewMessage_0059.png"
    pause 0.041
    Solid("#00000000")


style alt_menu_frame is empty
style alt_menu_vbox is vbox
style alt_menu_text is gui_text
style alt_menu_label is gui_label
style alt_menu_label_text:
    color '#FFFFFF'

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_button_text:
    size 60

style main_menu_frame:
    xsize 420
    yfill True

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")











screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background

    frame:
        style "game_menu_outer_frame"

        has hbox


        frame:
            style "game_menu_navigation_frame"

        frame:
            style "game_menu_content_frame"

            if scroll == "viewport":

                viewport:
                    yinitial yinitial

                    side_yfill True

                    has vbox
                    transclude

            elif scroll == "vpgrid":

                vpgrid:
                    cols 1
                    yinitial yinitial

                    scrollbars "vertical"
                    mousewheel True
                    edgescroll True
                    draggable True
                    pagekeys True

                    side_yfill True

                    transclude

            else:

                transclude

    use navigation

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 15
    right_padding 60

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 660
    right_margin 60
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45









screen aboutmenu():
    tag menu





    use game_menu(_("About"), scroll="viewport"):
        frame:
            vbox:

                xalign .5
                yalign .5
                spacing 45

        style_prefix "about"
        hbox:
            xsize 200
            ysize 400
            ypos 40
            spacing 20
            textbutton _("ABOUT"):
                text_hover_color "#888888"
                text_selected_color "#AAAAAA"
                action ShowMenu("about")

            textbutton _("ACTORS"):
                text_hover_color "#888888"
                text_selected_color "#AAAAAA"
                action ShowMenu("actors")

            textbutton _("ARTISTS"):
                text_hover_color "#888888"
                text_selected_color "#AAAAAA"
                action ShowMenu("artists")


        viewport:
            scrollbars "vertical" style_prefix "vbar"
            mousewheel True
            draggable True
            ypos -263
            side_yfill True
            has vbox
            transclude
    add Image("gui/about_feather.png")

screen about():
    tag menu
    style_prefix "about"
    use aboutmenu():
        vbox:
            text _("{color=#000000} \nThis video game is entirely based on real events, encounters, and personalities. \n \nAny content viewed as offensive is a reflection of American culture and not endorsed by Class of '09 or it's staff.\n\n\nApparently all characters depicted are over 18.\n\n\n\n\n\nThis program contains free software licensed under a number of licenses, including the GNU Lesser General Public License. A complete list of software is available at http://www.renpy.org/doc/html/license.html{/color} \n\n\n")

screen actors():
    tag menu
    use aboutmenu():
        hbox:
            spacing 20
            ypos -20
            xpos 50
            vbox:
                style_prefix "actor"
                text actor_credits
            vbox:
                style_prefix "char"
                text char_credits
define actor_credits = _("""
Elsie Lovelock
Kayli Mills
Max Field


Sarah Ruth Thomas
Anthony Sardinha
Marissa Lenti
Jordan Moore
Dreux Ferrano Jr.
Valerie Rose
Kira Buckland
Tiana Camacho
Lyle Rath
Corrine Sudberg
Griffin Puatu
Tom Schalk
Chris McCullough
Connor Quinn
Michael Potok
Katy Johnson
Joshua Gotay
Joe Boisits
Joshua Waters

Anna Kingsley
Brandon Winckler
Bryson Baugus
Belsheber Rusape
Lizzy Hofe
Michaela Laws
Krystal LaPorte

""")

define char_credits = _("""
NICOLE
JECKA
KYLAR
CRISPIN
JEFFERY
PRINCIPAL LYNN
COUNSELOR
MOM
MR. WHITE
COACH COLBY
EMILY
ARI
MEGAN
MR. BURLEDAY
KAREN
EMT
LAWYER
MR. KATZ
COP
HUNTER
KELLY
BRAXTON
TRODY
KYLE

ADD'L STUDENTS



""")

define artist_credits = _("""


{size=24}WRITTEN & DIRECTED BY{/size}
SBN3

{size=24}PROGRAMMERS{/size}
Carlos Ramirez
Dipesh Aggarwal

{size=24}LEAD ARTIST{/size}
Alesha Marie

{size=24}ARTISTS{/size}
Menii
Winston Wijanarko
Shawn Smith

{size=24}SCORED BY{/size}
Aaron Monroe
Hoobastankonia
""")

screen artists():
    tag menu
    style_prefix "artist"
    use aboutmenu():
        hbox:
            ypos -80
            xpos 170
            text artist_credits




define gui.about = ""

style artist_text:
    size 40
    color '#000000'
    text_align .5

style about_hbox:
    top_margin 50
    bottom_margin 25

style about_label:
    size 100

style about_label_text:
    size 100

style about_button:
    size 100

style about_button_text:
    size 60
    color '#000000'

style about_label_text:
    size 100

style char_text:
    color '#000000'
    size 28
    text_align 0.0

style char_hbox:
    top_margin 30

style actor_text:
    color '#000000'
    size 28
    text_align 1.0

style about_text:
    size 30
    color '#000000'










screen pause_save():
    tag menu


    use pause_file_slots(_("Save"))

screen save():
    tag menu


    use file_slots(_("Save"))


screen load():
    tag menu


    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Auto saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:




            order_reverse True


            button:
                style "page_label"

                key_events True
                xalign 0.5
                yalign 0.0
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value


            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.2

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)


            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 0.75

                spacing gui.page_spacing

                imagebutton:
                    idle "gui/arrowleft.png"
                    hover "gui/arrowleft.png"
                    action FilePagePrevious()


                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")


                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                imagebutton:
                    idle "gui/arrowright.png"
                    hover "gui/arrowright.png"
                    action FilePageNext()


screen pause_file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Auto saves"), quick=_("Quick saves"))

    add "gui/nvl.png"


    fixed:


        order_reverse True


        button:
            style "page_label"

            key_events True
            xalign 0.5
            yalign 0.0
            action page_name_value.Toggle()

            input:
                style "page_label_text"
                value page_name_value


        grid gui.file_slot_cols gui.file_slot_rows:
            style_prefix "slot"

            xalign 0.5
            yalign 0.2

            spacing gui.slot_spacing

            for i in range(gui.file_slot_cols * gui.file_slot_rows):

                $ slot = i + 1

                button:
                    action FileAction(slot)

                    has vbox

                    add FileScreenshot(slot) xalign 0.5

                    text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                        style "slot_time_text"

                    text FileSaveName(slot):
                        style "slot_name_text"

                    key "save_delete" action FileDelete(slot)


        hbox:
            style_prefix "page"

            xalign 0.5
            yalign 0.75

            spacing gui.page_spacing

            imagebutton:
                idle "gui/arrowleft.png"
                hover "gui/arrowleft.png"
                action FilePagePrevious()


            if config.has_autosave:
                textbutton _("{#auto_page}A") action FilePage("auto")

            if config.has_quicksave:
                textbutton _("{#quick_page}Q") action FilePage("quick")


            for page in range(1, 10):
                textbutton "[page]" action FilePage(page)

            imagebutton:
                idle "gui/arrowright.png"
                hover "gui/arrowright.png"
                action FilePageNext()

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")









screen preferences():
    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")




            null height (4 * gui.pref_spacing)

            vbox:
                style_prefix "slider"
                box_wrap True

                vbox:


                    if config.has_sound:

                        label _("{color=#000000}Scene Volume{/color}")

                        vbox:
                            bar value Preference("music volume")

                        label _("{color=#000000}UI Volume{/color}")

                        vbox:
                            bar value Preference("sound volume")


screen pause_prefs():
    tag menu


    add "gui/nvl.png"
    style_prefix "alt_menu"

    vbox:

        xalign 0.5
        yalign 0.5

        hbox:
            box_wrap True

            if renpy.variant("pc") or renpy.variant("web"):

                vbox:
                    style_prefix "radio"
                    label _("Display")
                    textbutton _("Window") action Preference("display", "window")
                    textbutton _("Fullscreen") action Preference("display", "fullscreen")





        null height (4 * gui.pref_spacing)

        vbox:
            style_prefix "slider"
            box_wrap True

            vbox:


                if config.has_sound:

                    label _("Scene Volume")


                    vbox:
                        bar value Preference("music volume")

                    label _("UI Volume")

                    vbox:
                        bar value Preference("sound volume")

                    textbutton _("Return") action Return()


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 675







screen help():
    tag menu


    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up\nClick Rollback Side")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")


    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.button_text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0















screen confirm(message, yes_action, no_action):


    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        has vbox
        xalign .5
        yalign .5
        spacing 45

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 150

            textbutton _("Sure") action yes_action
            textbutton _("Sorry, I'll keep playing.") action no_action



    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")









screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        has hbox
        spacing 9

        text _("Skipping")

        text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
        text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
        text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"



transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:


    font "DejaVuSans.ttf"









screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")









screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox
        spacing gui.nvl_spacing


        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)



        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            has fixed
            yfit gui.nvl_height is None

            if d.who is not None:

                text d.who:
                    id d.who_id

            text d.what:
                id d.what_id




define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")







style pref_vbox:
    variant "medium"
    xsize 675



screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        vbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"


style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_pref_vbox:
    variant "small"
    xsize None

style slider_pref_slider:
    variant "small"
    xsize 900

init python:
    import datetime

screen ending_tracker_screen():

    modal True

    default endings_name = {
        '0039': '703-359-4747    ',
        '0063': '703-359-4747    ',
        '0074': '703-359-4747    ',
        '0091': '703-359-4747    ',
        '0103': '703-359-4747    ',
        '0105': '703-359-4747    ',
        '0121': '703-250-2537    ',
        '0126': '703-359-4747    ',
        '0127': '703-359-4747    ',
        '0144': '703-359-4747    ',
        '0145': '703-359-4747    ',
        '0153': '703-359-4747    ',
        '0161': '703-359-4747    ',
        '0169': '703-359-4747    ',
        '0173': 'Jecka              ',
    }
    default endings_details = {
        '0039': 'announcement after announce...',
        '0063': 'I recall watching the news afte...',
        '0074': 'attention5is6privilege7',
        '0091': 'zzzzsdgsdg6sadhgdszfbadfb',
        '0103': 'I really do wonder sometimes if...',
        '0105': 'theanswerismaybejaajajajjaja...',
        '0121': 'priorirties year of our lord',
        '0126': 'you will never know who',
        '0127': 'i am the ball the ball the ball',
        '0144': 'EVERYthing works for EVERYone...',
        '0145': 'po551b1t135',
        '0153': 'dont look at me you fucking slut',
        '0161': 'they all run off after gettin...',
        '0169': 'fuck you',
        '0173': 'hey',
    }
    default ending_text = {
        '0039': 'announcement after announced on the intercom\n\n\"lets take a moment of silence for her\"\n\n\"its been one week\"\n\n\"its been one month\"\n\nso on and so forth\n\nno one hated her when she died,\nI wonder if the intercom would say my name that many times if I went early....',
        '0063': 'I recall watching the news after VT happened last april \n\nbetween the rambles of gun control an NRA member looked into the camera as if he was trying to talk to kids like me, im paraphrasing:\n\"if you are a student and feel alone, threatened, frightened, or inferior.. lashing out at the world with fatal violence like this is not the answer\"\n\nI dont want to kill them because im lonely, they just need a wake up call. most classes I sit alone, no one speaks to me. last week a girl who gets plenty of attention for her looks was venting to the teacher about how she didnt fit in.. mentioning she only knew her boyfriend and thats it... isnt that great irony?\nim lightyears from getting anything close to a girlfriend, she sees no one talks to me, yet vents right in front of me about how little she has socially.\n\nI am not jealous, just sick of the ignorance she and many others exhibit. their cozy little world, I want to destroy it.\nI want to destroy it and look them in the eye while I do it.\nI want them to remember me.',
        '0074': 'the biggest non factor in news i have ever heard in this school\n\n\n\n\n\n\nat least someone talks to you',
        '0091': '\ni lIke KilLinG People becAusE iT IS SO mUcH FUN it is moRE FUN THAN kilLiNg wILd gaME in tHe FOrreST BeCaUse man Is The most DAngerOUE ANaMal OF aLl TO kIll somEthINg giVes ME thE mOsT thriLLiNG expeRencE IT iS even BettEr tHan GeTtING yOuR ROCKS ofF witH a giRL thE besT pART oF iT IS ThAe WhEn i die I WILL Be REBOrN In PAradice AnD all thE i HavE KILLed WILL bEcOMe MY slAVeS i will NOT gIve yOU My NAME BeCAUsE yOU wIll trY To SlOi doWN oR atoP mY CoLlECtiOG Of SlaVeS FOR My AftErLife EBEORIeTemethHPIti',
        '0103': 'I really do wonder sometimes if I was the only one who joined for the feeling of friendship. feeling like a part of a clique.\n\nsure it is classified as a hate group, but it was the only group that pretended to love me.\n\nwhen you know youre HOPELESS, pretending is all you can HOPE for',
        '0105': 'can they call it a hate crime when everyone had to go???????????????????????????????????????????????????????????????????',
        '0121': 'kill and fuck a fat bitch',
        '0126': 'every video I post a comment, I actually post several\n\nnever my face on the profile picture\nnever a username that suggests who I might be\nnever the same account\n\nI post with the curiosity of seeing if that you would ever reach out to me, curious as to who I am like the rest of the world seems to be for you\n\nI hate you\nI think your an attention whore\nAnd yet I wish I had the acceptance and social stimuli you take for granted\n\nyou are such a fucking whore\n\nI could be your friend if you gave me a chance',
        '0127': 'its an interesting paradox\n\nwomen im not interested in tell me to be open with my emotions\nthey say its wrong that boys dont express their sadness and vulnerability\nbut the women who might consider me absolutely hate it. they think im a freak when i communicate any notion beside generosity\n\nthe world of the living is a game of paddleball...\nguess whos the ball',
        '0144': 'EVERYthing works for EVERYone but me EVERYtime\n\nim harassed they tell me to get over it\n\nsomeone desirable is harassed and they get the world as consolation',
        '0145': 'u wanna come over?\n\nu can stay with me : )',
        '0153': 'when i leave.. either for the day or forever.. it is always strange seeing them\n\nThey look and I look away, how dare they ask for eye contact when they wouldnt show me common decency when we were forced in a room together\n\ni go back in the car when i see someone from there, and i think about killing them :::: I think about killing a lot of people, i think about strapping them to a chair and beating their face into a pulp with an aluminum bat.\nive decided she doesnt deserve beauty',
        '0161': 'they all run off after getting their diplomas as the months go by I slowly start to realize they didnt talk to me and laugh at everything I said because they liked me, they did it to pass the time while they felt trapped in walls of boredom\n\nthis was the real world as I now knew it, not even admissions offices humored me without any extra curriculor clubs on my transcript... no one would ever let me in one. I have been working at a gas station to pass the time. Someone who laughed at me in school pulled up with a fancy car, trying to avoid eye contact as much as they could.\n\ndo they feel guilty? or maybe just past the point of looking for comic relief I guess 45 seconds at the pump isn\'t enough time for novelties like me',
        '0169': 'i have to hear about you and you arent even dead',
        '0173': 'miss u\n\nim sorry',
    }
    default selected_text = ""
    default show_popup = not persistent.seen_tip

    key "K_ESCAPE" action If(selected_text, true=SetScreenVariable("selected_text", ""), false=[Play("sound", "audio/Phone_close.mp3"), Hide("ending_tracker_screen")])
    key "K_BACKSPACE" action If(selected_text, true=SetScreenVariable("selected_text", ""), false=[Play("sound", "audio/Phone_close.mp3"), Hide("ending_tracker_screen")])

    add "gui/ending_tracker/ending_tracker_pda.png" at ending_tracker_pda

    fixed:

        at ending_tracker_screen

        add "gui/ending_tracker/base_screen.png"

        text "{}/15".format(len(persistent.endings)) font "joystix monospace.ttf" size 48 color "#ffffff" outlines [ (absolute(2), "#2370be", absolute(0), absolute(0)) ] xpos 405 ypos 129
        if len(persistent.endings) == 15:
            text "1/1" font "joystix monospace.ttf" size 48 color "#ffffff" outlines [ (absolute(2), "#2370be", absolute(0), absolute(0)) ] xpos 690 ypos 129
        else:
            textbutton _("0/1") text_font "joystix monospace.ttf" text_size 48 text_color "#ffffff" text_outlines [ (absolute(2), "#2370be", absolute(0), absolute(0)) ]:
                hovered SetScreenVariable("show_popup", True)
                action NullAction()
                padding (0, 0, 0, 0)
                xpos 690
                ypos 129

        text datetime.datetime.now().strftime("%I:%M %p") font "joystix monospace.ttf" size 48 color "#0000cc" xpos 1240 ypos 62

        if not selected_text:
            viewport:
                id "messages"
                xysize (1288, 618)
                xpos 260
                ypos 230
                draggable True
                mousewheel True

                if selected_text:
                    text ending_text[selected_text] font "texting2007.ttf" size 48 color "#000000"
                else:
                    vbox:
                        if len(persistent.endings) == 15:
                            button:
                                xysize (1288, 70)

                                hover_background "gui/ending_tracker/highlight_bar.png"

                                text "UNKNOWN          VIDEO MESSAGE" font "texting2007.ttf" size 48 color "#000000" yalign 0.5 xpos 25 yoffset 5:
                                    hover_color "#ffffff"

                                action Play("sound", "audio/Phone_button.mp3"), Start("scene_0999")

                        for ending in persistent.endings[::-1]:
                            $ ending = ending.split("_")[1]
                            $ detail = endings_details[ending]
                            button:
                                xysize (1288, 70)

                                hover_background "gui/ending_tracker/highlight_bar.png"

                                text "{}{}".format(endings_name[ending], detail) font "texting2007.ttf" size 48 color "#000000" yalign 0.5 xpos 25 yoffset 5:
                                    hover_color "#ffffff"

                                action Play("sound", "audio/Phone_button.mp3"), SetScreenVariable("selected_text", ending), SetScreenVariable("adj.value", 0.0)

            vbar value YScrollValue("messages"):
                xpos 1568
                ypos 245
                ysize 553
                xsize 40
                base_bar Solid("#00000000")
                thumb "gui/ending_tracker/texting_scrollbar.png"

        else:
            viewport:
                id "message_detail"
                xysize (1288, 628)
                xpos 260
                ypos 220
                draggable True
                mousewheel True

                text ending_text[selected_text] font "texting2007.ttf" size 48 color "#000000"

            vbar value YScrollValue("message_detail"):
                xpos 1568
                ypos 245
                ysize 553
                xsize 40
                base_bar Solid("#00000000")
                thumb "gui/ending_tracker/texting_scrollbar.png"

        imagebutton:
            idle "gui/ending_tracker/texting_back.png"
            hover "gui/ending_tracker/texting_back.png"

            action If(selected_text, true=[Play("sound", "audio/Phone_button.mp3"), SetScreenVariable("selected_text", "")], false=[Play("sound", "audio/Phone_close.mp3"), Hide("ending_tracker_screen")])
            xpos 264
            ypos 907

        add "gui/ending_tracker/screen_overlay.png"
        add "gui/ending_tracker/faceplate.png"

        if show_popup:
            button:
                xysize (447, 380)
                background "gui/ending_tracker/confirm_bubble.png"

                action NullAction()
                xpos 850
                ypos 115

                textbutton _("OK FUCK OFF"):
                    text_font "LeagueGothic-Regular.otf"
                    text_size 37
                    text_idle_color "#ff7cc0"
                    text_hover_color "#ffffff"
                    action SetScreenVariable("show_popup", False), SetField(persistent, "seen_tip", True)
                    xpos 300
                    ypos 308

transform ending_tracker_screen:
    alpha 0.0
    pause 0.3
    alpha 1.0

transform ending_tracker_pda:
    subpixel True
    xalign 0.915 yalign 0.835 zoom 0.112 alpha 0.0

    on show:
        parallel:
            linear 0.1 alpha 1.0
            pause 0.1
        parallel:
            pause 0.1
            linear 0.2 zoom 1.7 xalign .45 yalign 0.55

    on hide:
        parallel:
            linear 0.1 alpha 1.0
            pause 0.3
            linear 0.1 alpha 0.0
        parallel:
            linear 0.3 zoom 0.112 xalign 0.915 yalign 0.835
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
