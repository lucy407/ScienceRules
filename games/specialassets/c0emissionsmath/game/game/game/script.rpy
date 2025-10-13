define beginMarker = "0.0"
define sceneAudio = ""
define endMarker = "0.0"
define waitTime = "0.0"
define drift = 0.0
define waitTag = ""
define line = ""
define tolerance = 0.5
define pad = .05
define playback_paused = False
define paused_position = 0.0
define current_line = ""
define current_character = None
define line_time_remaining = 0.0
define pause_start = 0.0
define pause_duration = 0.0
define config.main_menu_music = "audio/menu_piano.mp3"

label splashscreen:
    $ renpy.movie_cutscene('logosplash.webm')
    return


init python:
    import time

    renpy.music.register_channel("ambient", "music", loop=True, tight=True)
    renpy.music.register_channel("vo", "music", loop=False, tight=True)
    renpy.music.register_channel("sfx", "music", loop=False, tight=True)

    def afterLoad():
        renpy.pause(1.0)

    config.after_load_callbacks = [afterLoad]
    preferences.show_empty_window = True

    if not persistent.endings:
        persistent.endings = []
        persistent.new_ending = False

    if not persistent.seen_tip:
        persistent.seen_tip = False

    def isclose(a, b, tolerance):
        return abs(a-b) < tolerance

    def seekvoice(event, interact=True, **kwargs):
        global beginMarker, tolerance, drift
        if event == 'begin':
            pos = renpy.music.get_pos('vo')
            if pos is None:
                pos = float(beginMarker)
                drift = 0.0
                renpy.music.play("<from " + beginMarker + ">" + sceneAudio,'vo')
                return
            drift = pos - float(beginMarker)
            if not isclose(pos, float(beginMarker), tolerance):
                renpy.music.play("<from " + beginMarker + ">" + sceneAudio,'vo')

    def setWait(begin, end):
        global beginMarker, endMarker, waitTime, waitTag, sceneAudio, current_line, drift
        beginMarker = str(begin)
        endMarker = str(end)
        waitTime = str((end - begin) - drift if drift >= 0 else (end - begin))
        waitTag = '{p=' + waitTime + '}{nw}'


    def setVoiceTrack(name):
        global sceneAudio, beginMarker, endMarker, waitTime
        sceneAudio = name
        beginMarker = "0.0"
        endMarker = "0.0"
        waitTime = "0.0"
        drift = 0.0
        renpy.music.play(sceneAudio,'vo')
        renpy.music.set_pause(False, channel='vo')

    def killAudio():
        renpy.music.set_pause(True, channel='vo')
        renpy.music.set_pause(True, channel='ambient')

    def speak(c, line, resume=False):
        global pause_duration, waitTag, current_line, current_character, line_time_remaining
        current_line = line
        current_character = c
        if not resume:
            renpy.pause(0.0)
            renpy.checkpoint(renpy.say(c, line + waitTag))
        else:
            pause_duration = 0
            line_time_remaining = 0
            renpy.say(c.name, line)
        
        if line_time_remaining > 0.0:
            p = line_time_remaining
            
            line_time_remaining = 0
            current_line = current_line.split("{p")[0]
            if pause_duration >= p:
                speak(c, current_line + '{p=' + str(p) + '}{nw}', True)
            else:
                speak(c, current_line + '{p=' + str(pause_duration) + '}{nw}', True)



    def game_unpause():
        global pause_duration
        if pause_duration > 0:
            pause_duration += time.time() - pause_start
        else:
            pause_duration = time.time() - pause_start
        renpy.return_statement()

    def ending_reached(ending):
        import os
        import shutil
        ending_map = {
            '0039': 'shut up about this bitch4.txt',
            '0063': 'they just dont get it and never will.txt',
            '0074': 'attention5is6privilege7.txt',
            '0091': 'sdgsdg6sadhgdszfbadfb6adzfghzdfh6.txt',
            '0103': 'victims 2006 breed 2008 victims i want to kill myself look at me.txt',
            '0105': 'theanswerismaybejaajajajjajajaja.txt',
            '0121': 'priorirties in the year of our lord 2007.txt',
            '0126': 'she will never know who and its not fine.txt',
            '0127': 'i am the ball the ball the ball.txt',
            '0144': '3y3roll hardddddddddd.txt',
            '0145': 'po551b1t135.txt',
            '0153': 'dont do not look dont look at me i dont want it.txt',
            '0161': 'what about me, what ABOUT me 2010.txt',
            '0169': 'so close yet so 4375457far.txt',
            '0173': 'happy659087i5607905.txt',
        }
        desktop_path = os.path.expanduser("~/Desktop/")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(renpy.loader.transfn('endings/completed.txt'), 'r') as fp:
            endings = fp.read().splitlines()
            if ending not in endings:
                shutil.copy(renpy.loader.transfn('endings/' + ending_map[ending]), desktop_path)
        
        with open(renpy.loader.transfn('endings/completed.txt'), 'a') as fp:
            fp.writelines(["\n" + ending])

    def game_pause():
        global paused_position, endMarker, line_time_remaining, pause_start
        renpy.music.set_pause(True, channel='vo')
        renpy.music.set_pause(True, channel='ambient')
        pause_start = time.time()
        paused_position = renpy.music.get_pos('vo')
        line_time_remaining = float(endMarker) - paused_position if paused_position is not None else 0

init:

    $ config.enter_transition = None
    image black = Solid((0, 0, 0, 255))


transform transform_logo:
    alpha 0 xalign 1.2 yalign 0.2 size (580.0,395.0) subpixel True
    easein 1.0 alpha 1 xalign 0.88

screen pause_menu():
    tag menu

    on "show":
        action Function(game_pause)

    key "K_ESCAPE" action Function(game_unpause)
    key "mouseup_3" action Function(game_unpause)
    key "K_MENU" action Function(game_unpause)


    add "gui/nvl.png"
    style_prefix "main_menu"

    zorder 100

    hbox:
        frame:
            style "main_menu"

    add "gui/ClassOf09logo.png" at transform_logo

    vbox:

        xalign 0.5
        yalign 0.5


        textbutton _("Resume"):
            activate_sound "audio/MainMenuPress.mp3"
            hover_sound "audio/MainMenuRollover.mp3"
            action Function(game_unpause)
        textbutton _("Options"):
            activate_sound "audio/MainMenuPress.mp3"
            hover_sound "audio/MainMenuRollover.mp3"
            action ShowMenu('pause_prefs')
        textbutton _("Save"):
            activate_sound "audio/MainMenuPress.mp3"
            hover_sound "audio/MainMenuRollover.mp3"
            action ShowMenu('pause_save')

        textbutton _("Main Menu"):
            activate_sound "audio/MainMenuPress.mp3"
            hover_sound "audio/MainMenuRollover.mp3"
            action [Stop("vo"),Stop("ambient"),MainMenu()]

style pause_menu_button_text:
    size 200

style skip_button_text:
    size 50


screen disable_Controls():
    tag menu
    zorder 0

    key "mouseup_1" action NullAction()
    key "mouseup_2" action NullAction()
    key "mouseup_3" action NullAction()
    key "K_ESCAPE" action NullAction()
    key "K_MENU" action NullAction()
    style_prefix "skip"

    vbox:
        spacing -5

        xalign 0.92
        yalign 1.0

        textbutton "Skip" action [Jump ("scene_0002"), Hide("disable_Controls")]


screen disable_controls_for_ending():
    tag menu
    zorder 0
    key "K_ESCAPE" action NullAction()
    key "K_MENU" action NullAction()

    key "K_UP" action NullAction()
    key "K_DOWN" action NullAction()
    key "K_LEFT" action NullAction()
    key "K_RIGHT" action NullAction()
    key "K_SPACE" action NullAction()

    key "a" action NullAction()
    key "b" action NullAction()
    key "c" action NullAction()
    key "d" action NullAction()
    key "e" action NullAction()
    key "f" action NullAction()
    key "g" action NullAction()
    key "h" action NullAction()
    key "i" action NullAction()
    key "j" action NullAction()
    key "k" action NullAction()
    key "l" action NullAction()
    key "m" action NullAction()
    key "n" action NullAction()
    key "o" action NullAction()
    key "p" action NullAction()
    key "q" action NullAction()
    key "r" action NullAction()
    key "s" action NullAction()
    key "t" action NullAction()
    key "u" action NullAction()
    key "v" action NullAction()
    key "w" action NullAction()
    key "x" action NullAction()
    key "y" action NullAction()
    key "z" action NullAction()

    key "0" action NullAction()
    key "1" action NullAction()
    key "2" action NullAction()
    key "3" action NullAction()
    key "4" action NullAction()
    key "5" action NullAction()
    key "6" action NullAction()
    key "7" action NullAction()
    key "8" action NullAction()
    key "9" action NullAction()


define NICOLE = Character("Nicole", callback=seekvoice)
define KYLAR = Character("Kylar", callback=seekvoice)
define GIRL_1 = Character("Ari", callback=seekvoice)
define CRISPIN = Character("Crispin", callback=seekvoice)
define GUY_1 = Character("Trody", callback=seekvoice)
define JEFFERY = Character("Jeffery", callback=seekvoice)
define TEACHER_1 = Character("Mr. Burleday", callback=seekvoice)
define JECKA = Character("Jecka", callback=seekvoice)
define MOM = Character("Mom", callback=seekvoice)
define GAMER_BROTHER = Character("Gamer Brother", callback=seekvoice)
define COP = Character("Cop", callback=seekvoice)
define COACH = Character("Coach Colby", callback=seekvoice)
define MR_WHITE = Character("Mr. White", callback=seekvoice)
define GUY_2 = Character("Kyle", callback=seekvoice)
define GIRL_2 = Character("Emily", callback=seekvoice)
define LYNN = Character("Principal Lynn", callback=seekvoice)
define GUY_3 = Character("Hunter", callback=seekvoice)
define GIRL_3 = Character("Megan", callback=seekvoice)
define COUNSELOR = Character("Counselor", callback=seekvoice)
define TEACHER_2 = Character("Mr. Katz", callback=seekvoice)
define GIRL_4 = Character("Karen", callback=seekvoice)
define GUY_5 = Character("Braxton", callback=seekvoice)
define GIRL_5 = Character("Kelly", callback=seekvoice)
define EMT = Character("EMT", callback=seekvoice)
define LAWYER = Character("Lawyer", callback=seekvoice)
define none = Character("none", callback=seekvoice)
define BAND = Character("Guy with a drug problem", callback=seekvoice)
define WPP = Character("WPP Kids", callback=seekvoice)

image gamer_brother flipped = im.Flip("gamer_brother.png", horizontal=True)
image gamer_brother upset flipped = im.Flip("gamer_brother upset.png", horizontal=True)
image nicole flipped = im.Flip("nicole.png", horizontal=True)
image nicole angry flipped = im.Flip("nicole angry.png", horizontal=True)
image nicole shirt flipped = im.Flip("nicole shirt.png", horizontal=True)
image nicole shirt angry flipped = im.Flip("nicole shirt angry.png", horizontal=True)
image nicole tanktop flipped = im.Flip("nicole tanktop.png", horizontal=True)
image nicole tanktop angry flipped = im.Flip("nicole tanktop angry.png", horizontal=True)
image crispin flipped = im.Flip("crispin.png", horizontal=True)
image crispin unhappy flipped = im.Flip("crispin unhappy.png", horizontal=True)
image nicole shirt flipped = im.Flip("nicole shirt.png", horizontal=True)
image nicole tanktop flipped = im.Flip("nicole tanktop.png", horizontal=True)
image girl_1 flipped = im.Flip("girl_1.png", horizontal=True)
image kylar flipped = im.Flip("kylar.png", horizontal=True)
image kylar unhappy flipped = im.Flip("kylar unhappy.png", horizontal=True)
image teacher_1 flipped = im.Flip("TEACHER_1.png", horizontal=True)
image teacher_1 angry flipped = im.Flip("TEACHER_1 angry.png", horizontal=True)
image guy_1 flipped = im.Flip("guy_1.png", horizontal=True)
image cop flipped = im.Flip("cop.png", horizontal=True)
image jeffery flipped = im.Flip("jeffery.png", horizontal=True)
image jeffery angry flipped = im.Flip("jeffery angry.png", horizontal=True)
image mom flipped = im.Flip("mom.png", horizontal=True)
image jecka flipped = im.Flip("jecka.png", horizontal=True)
image nicole tanktop smile flipped = im.Flip("nicole tanktop smile.png", horizontal=True)


transform leftstage:
    xalign 0.0

transform leftcenterstage:
    xalign 0.33

transform centerstage:
    xalign 0.5

transform rightcenterstage:
    xalign 0.66

transform rightstage:
    xalign 1.0

transform off_right:
    xalign 1.4

transform off_left:
    xalign -0.4

transform off_farright:
    xalign 1.6

transform off_farleft:
    xalign -0.73
transform percsuperleft:
    xalign 0.228
    yalign 0.7

transform percrightcenter:
    xalign 0.65
    yalign 0.7

transform percfall:
    xalign 0.45
    yalign 5

transform percnotasright:
    xalign 0.56
    yalign 0.7

transform percentrist:
    xalign 0.45
    yalign 0.7

transform percleftstage:
    xalign 0.456
    yalign 0.7

image opening cutscene = Movie(play="opening.webm")

image percpop = Movie (play="percpop.webm")

image 0039end = Movie (play="0039end.webm", loop=False)

image 0063end = Movie (play="0063end.webm", loop=False)

image 0074end = Movie (play="0074end.webm", loop=False)

image 0091end = Movie (play="0091end.webm", loop=False)

image 0103end = Movie (play="0103end.webm", loop=False)

image 0105end = Movie (play="0105end.webm", loop=False)

image 0121end = Movie (play="0121end.webm", loop=False)

image 0126end = Movie (play="0126end.webm", loop=False)

image 0127end = Movie (play="0127end.webm", loop=False)

image 0144end = Movie (play="0144end.webm", loop=False)

image 0145end = Movie (play="0145end.webm", loop=False)

image 0153end = Movie (play="0153end.webm", loop=False)

image 0161end = Movie (play="0161end.webm", loop=False)

image 0169end = Movie (play="0169end.webm", loop=False)

image 0173end = Movie (play="0173end.webm", loop=False)

label start:
    stop music fadeout 0.7
    $ quick_menu = False
    $ _game_menu_screen = "pause_menu"
    show black
    show opening cutscene
    show screen disable_Controls
    $ renpy.pause(140,hard=True)
    jump scene_0002

label scene_0002:
    hide screen disable_Controls

    $ setVoiceTrack("audio/Scenes/0002.mp3")

    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 1
    scene onlayer master
    show black

    show title_september2007 onlayer screens:
        alpha 0.0
        linear .2 alpha 1

    show school front with Pause(2.252):
        zoom 1.0 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.627 zoom 1.1 truecenter

    scene school int 1
    hide title_september2007 onlayer screens

    show guy_1:
        xzoom -1
        leftcenterstage
        pause 3.8
        linear 3.3 off_right

    show girl_2 color3:
        xzoom -1
        off_left
        linear 6 off_right
    show girl_1:
        rightstage

    $ quick_menu = True

    show kylar:
        off_right
        linear 2.5 rightcenterstage
    play ambient "audio/Ambience/Hallway_Ambience.mp3"

    $ setWait(2.627,8.258)
    $ speak(KYLAR, "Hey so for the senior prank this year what if we like parked our cars where we don't usually park them!")

    show kylar:
        rightcenterstage

    $ setWait(8.258,10.093)
    $ speak(GIRL_1, "Oh my god that is so funny!")

    show kylar:
        rightcenterstage
        linear 6.0 off_left

    show girl_1:
        rightstage
        5.0
        linear 1.5 off_right

    show nicole angry:
        off_left
        5.0
        linear 3.0 leftcenterstage

    $ setWait(10.093,16.307)
    $ speak(KYLAR, "Heh yeah math class this year with Mr. Burleday huh yeah like fuck Mr. Burleday dude ha ha ha ha!")
    $ setWait(16.307,21.229)
    $ speak(NICOLE, "God they are never funny. It's like the girls just laugh to avoid sexual assault.")

    show crispin:
        off_right
        linear 3.0 xalign 0.71
    show nicole angry:
        leftcenterstage

    show kylar:
        off_left
    $ setWait(21.229,23.69)
    $ speak(CRISPIN, "Hey yo you new to this educational prison?")

    show nicole:
        leftcenterstage

    show girl_1:
        off_right
    $ setWait(23.69,26.234)
    $ speak(NICOLE, "Ha ha ha ha ha wow yeah that was funny.")

    show kylar:
        off_left
    $ setWait(26.234,31.99)
    $ speak(CRISPIN, "Yeah I'm getting into like humor and stuff-- anyway you know anyone around here? Know where your classes are?")




    show crispin:
        xalign 0.71

    $ setWait(31.99,36.1)
    $ speak(NICOLE, "I mean kinda, there's like numbers on the doors I think I can figure it out.")

    $ setWait(36.1,41.958)
    $ speak(CRISPIN, "No no no no no I could show you around. Like a school tour? You wanna do that? You up for that?")

menu:
    "HUMOR THE SCHOOL TOUR":
        jump scene_0003
    "DECLINE AND GO STRAIGHT TO CLASS":
        jump scene_0004
    "TELL HIM OFF AND CUT CLASS":
        jump scene_0005
label scene_0003:
    $ setVoiceTrack("audio/Scenes/0003.mp3")
    play ambient "audio/Ambience/School_Ext_Ambience.mp3"

    scene school courtyard

    show nicole:
        xalign -0.7
        linear 8 leftstage

    show crispin flipped:
        off_left
        linear 8 leftcenterstage

    $ setWait(0.289,8.755)

    $ speak(CRISPIN, "Yeah so then my friend got the DLC, that's downloadable content, it's like 10 dollars like dude kinda not worth it for the gun.")
    $ setWait(8.755,12.092)

    $ speak(NICOLE, "Why are you talking to me about video games?")
    $ setWait(12.092,17.306)

    show crispin unhappy:
        leftcenterstage

    show nicole:
        leftstage

    $ speak(CRISPIN, "Just something y'know... uh.. what you don't like play video games or something?")
    $ setWait(17.306,24.146)
    $ speak(NICOLE, "I'm a thin girl do I fucking look like I play video games? I'd rather play dead at a necrophilia convention.")
    $ setWait(24.146,29.568)
    $ speak(CRISPIN, "Oh.. well... yeah y'know...")
    $ setWait(29.568,31.82)
    $ speak(NICOLE, "I know what?")
    $ setWait(31.82,36.366)
    $ speak(CRISPIN, "Did.. did you hear about how Mountain Dew makes guys sterile?")
    $ setWait(36.366,40.871)
    $ speak(NICOLE, "Yeah, from you and every other guy who reads the internet to try to be interesting.")
    $ setWait(40.871,44.917)


    $ speak(GUY_1, "Ha nice rollie backpack you fuckin' four-eyed double dick suckin' bitch!")
    $ setWait(44.917,49.129)
    show nicole:
        leftstage
        linear 0.3 off_farleft

    show crispin:
        leftcenterstage
        linear 0.3 off_left

    show jeffery angry:
        off_farright
        linear 0.3 rightstage

    show guy_1 flipped:
        off_right
        linear 0.3 rightcenterstage


    $ speak(JEFFERY, "Hey stop kicking it, this backpack holds priceless reading materials!")
    $ setWait(49.129,52.799)
    $ speak(GUY_1, "Oh yeah like what? The Bernstein Bears Make Eye Contact?")
    $ setWait(52.799,58.597)
    $ speak(JEFFERY, "Hey what is this? 4th grade? It is home to some of my favorite manga books.")
    $ setWait(58.597,60.974)
    $ speak(GUY_1, "Manga... What is that like Asian or something?")
    $ setWait(60.974,66.897)
    $ speak(JEFFERY, "Japanese thank you! Some of which go on to be very popular television shows.")
    $ setWait(66.897,71.151)
    $ speak(GUY_1, "Wait can't you watch half of those on cartoon channels? Why the hell would you read it?")
    $ setWait(71.151,73.529)
    $ speak(JEFFERY, "Rggghh! That's it!")
    $ setWait(73.529,76.573)

    show nicole:
        xalign -0.5
        linear 2 leftcenterstage


    $ speak(NICOLE, "Dude how do you care about anything this much?")
    $ setWait(76.573,77.783)

    show guy_1:
        rightcenterstage

    show crispin flipped:
        off_farleft
        linear 4 leftstage

    show jeffery:
        rightstage

    $ speak(JEFFERY, "What do you mean?")
    $ setWait(77.783,81.787)

    show guy_1:
        rightcenterstage

    $ speak(NICOLE, "Like okay he thinks your Chinese cartoon books are stupid, why defend it?")
    $ setWait(81.787,85.749)
    $ speak(JEFFERY, "Stay out of this you.. you girl!")
menu:
    "DOUBLE DOWN ON THE VERBAL ABUSE":
        jump scene_0006
    "WATCH HIM GET BEAT UP":
        jump scene_0007
label scene_0004:
    $ setVoiceTrack("audio/Scenes/0004.mp3")
    scene school int 1
    show crispin:
        xalign 0.71

    show nicole:
        leftcenterstage
    $ setWait(0.029,7.345)
    $ speak(NICOLE, "School tour um... that sounds nicely mediocre but I'm just gonna go to class, see ya.")
    $ setWait(7.345,14.018)
    show nicole flipped:
        leftcenterstage
        linear 4 off_left

    $ speak(CRISPIN, "Oh well yeah I'm Crispin by the way. Yeah we should hang out some time. Yeah okay! Alright bye yeah!")
    $ setWait(14.018,19.273)


    scene classroom int 2
    play ambient "audio/Ambience/Classroom_Ambience.mp3"


    show teacher_1:
        leftcenterstage

    show nicole:
        off_left
        linear 2 leftstage

    $ speak(TEACHER_1, "Oh you must be new. Yes please take a seat next to Jeffery.")
    $ setWait(19.273,20.983)

    show teacher_1:
        leftcenterstage
        linear 1.6 off_left

    show nicole:
        leftstage
        linear 2 rightcenterstage

    show jeffery happy:
        off_right
        linear 1 rightstage

    $ speak(JEFFERY, "Hey.")
    $ setWait(20.983,22.819)
    $ speak(NICOLE, "...")
    $ setWait(22.819,29.325)
    $ speak(JEFFERY, "Hey so uh... I guess... I guess we're lab partners huh?")
    $ setWait(29.325,31.619)
    $ speak(NICOLE, "I guess.")
    $ setWait(31.619,33.496)

    $ speak(JEFFERY, "Not a big talker, are ya?")
    $ setWait(33.496,37.083)

    $ speak(NICOLE, "I don't know you. Are you just chummy with everyone you meet?")
    $ setWait(37.083,41.754)

    $ speak(JEFFERY, "Not everyone. But if they look the type to like anime then may as well, right?")
    $ setWait(41.754,44.924)

    show nicole:
        rightcenterstage
        linear 1 leftcenterstage

    $ speak(NICOLE, "I'm sorry, I look like I like anime? How do I fix that?")
    $ setWait(44.924,49.137)

    show jeffery:
        rightstage
        linear 1 rightcenterstage

    $ speak(JEFFERY, "No no that's a good thing! It means you're cool and different.")
    $ setWait(49.137,50.638)

    $ speak(NICOLE, "...And 300 pounds.")
    $ setWait(50.638,51.264)

    $ speak(JEFFERY, "What was that?")
    $ setWait(51.264,55.101)

    $ speak(NICOLE, "Oh nothing was just converting British currency in my head.")
    $ setWait(55.101,60.314)

    $ speak(JEFFERY, "Cool, see? Um, well the teacher said I'm Jeffery, what's your name?")
menu:
    "THIS FREAK IS NOT GETTING MY NAME":
        jump scene_0008
    "PRETEND TO BE NICE":
        jump scene_0009
label scene_0005:
    $ setVoiceTrack("audio/Scenes/0005.mp3")


    scene school int 1

    show nicole:
        leftcenterstage

    show crispin:
        xalign 0.71

    $ setWait(0.053,5.003)

    $ speak(NICOLE, "I'm gonna be honest, you seem like the most boring piece of shit I've ever met.")
    $ setWait(5.003,5.754)
    show crispin unhappy:
        xalign 0.71
    $ speak(CRISPIN, "Huh?")
    $ setWait(5.754,12.844)
    $ speak(NICOLE, "Well wait, most I've ever met would mean you stand out in some way. You're a very run of the mill waste of time.")
    $ setWait(12.844,15.18)
    $ speak(CRISPIN, "I don't get it, what'd I do?")
    $ setWait(15.18,17.39)
    $ speak(NICOLE, "You have time for the whole list?")
    $ setWait(17.39,18.141)
    $ speak(CRISPIN, "I guess--")
    $ setWait(18.141,25.482)
    $ speak(NICOLE, "First you wear classic rock T-shirts from Walmart. Girls don't compliment how you dress so you settled for old people hi-fiving you for being retro.")
    $ setWait(25.482,27.484)
    $ speak(CRISPIN, "Nah people think I'm cool--")
    $ setWait(27.484,34.722)
    $ speak(NICOLE, "Rapid fire of assumptions, tell me if I get any wrong. You call your bicycle a BMX, like energy drinks, take pictures of your skateboarding wounds...")
    $ setWait(34.722,41.122)
    $ speak(NICOLE, "...mention to anyone they can't get addicted to marijuana, and own a guitar pick necklace.")
    $ setWait(41.122,46.002)

    show nicole:
        leftcenterstage
        pause 1.5
        linear 2 off_right

    $ speak(CRISPIN, "Well... alright I'll see you later then.")
    $ setWait(46.002,48.379)

    scene school int 2

    show nicole:
        off_left
        linear 3 leftcenterstage

    show kylar:
        rightstage
        linear 1 rightcenterstage

    $ speak(KYLAR, "Hey I've seen your ass around here before.")
    $ setWait(48.379,50.131)
    $ speak(NICOLE, "It's my first day, you sure about that?")
    $ setWait(50.131,52.342)
    $ speak(KYLAR, "Whatever all you hot girls look the same.")
    $ setWait(52.342,53.843)
    $ speak(NICOLE, "That was real discreet.")
    $ setWait(53.843,57.096)
    $ speak(KYLAR, "Gotta be, especially cutting under this school's security.")
    $ setWait(57.096,57.847)
    $ speak(NICOLE, "Uh huh.")
    $ setWait(57.847,61.976)
    $ speak(KYLAR, "And a girl like you skipping the first day? Are you bad bitch or what?")
    $ setWait(61.976,63.561)
    $ speak(NICOLE, "I'm an abysmal bitch.")
    $ setWait(63.561,67.732)
    $ speak(KYLAR, "Fuckin' cool rock on. So what do you do here? Like cheerleading?")
    $ setWait(67.732,69.15)
    $ speak(NICOLE, "Doesn't pay so no.")
    $ setWait(69.15,76.324)
    $ speak(KYLAR, "Well I'm on the lacrosse team. Last season we went 7-5 like above 500 not bad. It's my life pretty much.")
    $ setWait(76.324,80.787)
    $ speak(NICOLE, "How can you make lacrosse your life? There's no pro league for it, is there?")
    $ setWait(80.787,90.38)
    $ speak(KYLAR, "Well.. I'm sure they're out there. Besides we only lost 5 games cause I fucked up my knee and couldn't play the rest of the season. But it's pretty bad ass cause they keep giving me Percocet.")
    $ setWait(90.38,92.632)
    $ speak(NICOLE, "Cool, seriously? How much?")
    $ setWait(92.632,99.43)
    $ speak(KYLAR, "Enough to demotivate an elephant. I got 'em right here you wanna do 'em with me? They only kinda get you fucked up but it's good.")
    menu:
        "DECLINE HIS FREE DRUGS":
            jump scene_0010
        "POP PERCS WITH HIM":
            jump scene_0011
label scene_0006:
    $ setVoiceTrack("audio/Scenes/0006.mp3")
    scene school courtyard

    show nicole angry:
        leftcenterstage

    show jeffery:
        rightstage

    show crispin unhappy flipped:
        leftstage

    show guy_1:
        rightcenterstage

    $ setWait(0.202,2.788)
    $ speak(NICOLE, "What the fuck you greasy bitch I was trying to help you.")
    show jeffery angry:
        rightstage
    $ setWait(2.788,7.793)
    $ speak(JEFFERY, "I don't need help from someone who misnationalizes my Japanese manga books!")
    $ setWait(7.793,10.88)

    show guy_1 flipped:
        rightcenterstage

    $ speak(GUY_1, "\"Japanese manga books\" that's literally you, that's what you sound like.")
    $ setWait(10.88,15.343)
    $ speak(NICOLE, "Yeah first time you talk to a girl and you correct her on the origin of your backwards picture books.")
    $ setWait(15.343,18.888)
    $ speak(JEFFERY, "They're not backwards they just read right-to-left!")
    $ setWait(18.888,20.222)
    $ speak(GUY_1, "No one cares!")
    $ setWait(20.222,30.983)
    $ speak(JEFFERY, "I care! And the Youtube anime community cares too! Like NaruParty13 he's got 1,600 subscribers, do you have that many?")
    show nicole:
        leftcenterstage
    $ setWait(30.983,33.444)
    $ speak(NICOLE, "Why would you upload videos to Youtube?")
    $ setWait(33.444,35.988)
    $ speak(JEFFERY, "How else do you think videos get there?")
    $ setWait(35.988,42.078)
    $ speak(NICOLE, "It's for watching TV shows, you don't fucking participate in it. What am I gonna go on Youtube and get digitally molested?")
    $ setWait(42.078,44.497)
    $ speak(JEFFERY, "No it- ughhh!")
    $ setWait(44.497,46.332)
    $ speak(GUY_1, "Ha ha ha you gonna transform?")
    $ setWait(46.332,53.047)
    $ speak(JEFFERY, "Whatever everything's fine! My Mom said the bullies go nowhere and smart kids like me become notable adults.")

    $ setWait(53.047,61.013)
    $ speak(NICOLE, "The most notable thing you could do is killing yourself before graduation. Then your Dad can cry in front of school assemblies next to a black and white photo of you.")
    show crispin unhappy:
        leftstage
        linear 2.2 off_left
    $ setWait(61.013,63.766)
    $ speak(JEFFERY, "Wha- ...no...")
    $ setWait(63.766,64.642)
    $ speak(GUY_1, "Little bitch.")

    show jeffery angry flipped:
        rightstage
        linear 1.5 off_farright
    $ setWait(64.642,68.354)
    $ speak(JEFFERY, "Wahhh!! I'm straight!")

    show guy_1:
        rightcenterstage
    $ setWait(68.354,71.649)
    $ speak(GUY_1, "So hey you're like pretty cool, what's your name?")
    $ setWait(71.649,74.443)
    $ speak(NICOLE, "Well my last name's \"You\". Most people just call me that.")
    $ setWait(74.443,76.779)
    $ speak(GUY_1, "You? What is that like Asian? That's hot.")
    $ setWait(76.779,78.656)
    $ speak(NICOLE, "Yeah Grandma had yellow fever.")
    $ setWait(78.656,81.7)
    $ speak(GUY_1, "Cool yeah... So what's your first name?")
    $ setWait(81.7,83.035)
    $ speak(NICOLE, "Fuck.")

    stop ambient fadeout 1
    jump scene_0014
label scene_0007:
    window show
    $ setVoiceTrack("audio/Scenes/0007.mp3")
    scene school courtyard

    show nicole:
        leftcenterstage

    show jeffery angry:
        rightstage

    show crispin unhappy flipped:
        leftstage

    show guy_1:
        rightcenterstage

    $ setWait(0.165,1.5)

    $ speak(NICOLE, "I'll just let this play out.")

    show guy_1 flipped:
        rightcenterstage

    $ setWait(1.5,3.419)

    $ speak(GUY_1, "I should beat your ass for liking anime.")

    show jeffery:
        rightstage

    $ setWait(3.419,5.087)

    $ speak(JEFFERY, "Wha- what're you talking about?")

    show nicole sly:
        leftcenterstage

    $ setWait(5.087,6.255)
    $ speak(NICOLE, "Yeah do it, I'm bored.")

    show crispin flipped:
        leftstage
    $ setWait(6.255,7.881)
    $ speak(CRISPIN, "Yeah do it yeah yeah.")

    show jeffery:
        rightstage

    show guy_1 flipped:
        rightcenterstage
        linear 3 rightstage
    show black onlayer screens:
        alpha 0.0
        linear 1 alpha 1.0
        1.8
        linear 0.8 alpha 0.0

    stop ambient fadeout 1

    $ setWait(7.881,10.259)
    $ speak(JEFFERY, "Don't pull my hair!")

    show guy_1 flipped:
        rightcenterstage
    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 1

    show jeffery broken:
        rightstage
    $ setWait(10.259,12.386)
    $ speak(GUY_1, "Ah I broke his glasses, I gotta split!")

    show jeffery broken:
        rightstage
    show guy_1 flipped:
        rightcenterstage
        pause 2.4
        linear 0.9 off_farright

    show crispin unhappy flipped:
        leftstage
        pause 2.4
        linear 1.6 off_right

    $ setWait(12.386,16.682)
    $ speak(CRISPIN, "Oh yeah me too I'm on probation, I'll catch you around!")

    show jeffery broken:
        rightstage
        linear 2 rightcenterstage

    $ setWait(16.682,18.684)
    $ speak(JEFFERY, "...Why aren't you running off with them?")

    show nicole:
        leftcenterstage

    $ setWait(18.684,21.645)

    $ speak(NICOLE, "They're pussies, I'm not afraid to watch someone grovel in pain.")
    $ setWait(21.645,28.569)
    $ speak(JEFFERY, "Well they're all just assholes. That guy's been making fun of me for liking anime since the 6th grade.")
    $ setWait(28.569,30.696)
    $ speak(NICOLE, "Then just stop liking anime?")
    $ setWait(30.696,35.534)
    $ speak(JEFFERY, "But I can't do that, anime is my favorite thing ever, my life!")
    $ setWait(35.534,40.748)
    $ speak(NICOLE, "How are you emotionally invested in consumption? Are you trying to make anime? I don't get it.")
    $ setWait(40.748,46.378)
    $ speak(JEFFERY, "Kinda, I make fan art based on the works of Sento Takahashi")
    $ setWait(46.378,49.423)
    $ speak(NICOLE, "You know that anime will exist with or without you, right?")
    $ setWait(49.423,52.051)
    $ speak(JEFFERY, "No! Wait what do you mean?")
    $ setWait(52.051,57.473)
    $ speak(NICOLE, "Like Senti Takimokey whatever the fuck his name is, if you died he wouldn't care, he wouldn't even know.")
    $ setWait(57.473,58.807)
    $ speak(JEFFERY, "What's your point?")
    $ setWait(58.807,61.81)
    $ speak(NICOLE, "How do you give a fuck about anything that doesn't give a fuck about you?")
    $ setWait(61.81,69.151)
    $ speak(JEFFERY, "Hey in a translated newsletter he said \"thank you\" to each and every one of his fans! That includes me!")
    $ setWait(69.151,70.736)
    $ speak(NICOLE, "Oh he writes in English?")
    $ setWait(70.736,73.614)
    $ speak(JEFFERY, "No his fan club translated it from Japanese.")
    $ setWait(73.614,77.91)
    $ speak(NICOLE, "That's my point. He can't even talk to you, you think he cares about you?")
    $ setWait(77.91,80.079)
    $ speak(JEFFERY, "Well.. uh..")
    $ setWait(80.079,84.083)
    $ speak(NICOLE, "Anyway, you wanna stick to getting beat up over children's media? I'll leave you to it.")
    $ setWait(84.083,84.958)
    $ speak(JEFFERY, "Wait!")
    $ setWait(84.958,86.752)
    $ speak(NICOLE, "Huh what?")
    $ setWait(86.752,91.215)
    $ speak(JEFFERY, "...Thanks for talking to me. Not many people are as nice to me as you are.")
    show nicole angry:
        leftcenterstage
    $ setWait(91.215,93.467)
    $ speak(NICOLE, "That was nice to you? God dammit.")
    $ setWait(93.467,97.179)
    $ speak(JEFFERY, "Yeah I'm Jeffery by the way. What's your name?")
    $ setWait(97.179,99.056)
    $ speak(NICOLE, "Ugh.. Nicole.")
    $ setWait(99.056,102.059)
    $ speak(JEFFERY, "Wow.. okay.. bye Nicole.")

    show nicole angry flipped:
        leftcenterstage
        linear 3 off_left
    $ setWait(102.059,103.268)
    $ speak(NICOLE, "Yeah yeah okay.")
    stop ambient fadeout 1
    jump scene_0014
label scene_0008:


    $ setVoiceTrack("audio/Scenes/0008.mp3")

    scene classroom int 2

    show nicole angry:
        leftcenterstage

    show jeffery:
        rightcenterstage


    $ setWait(0.251,3.88)

    $ speak(NICOLE, "What so you can look me up on MySpace or something? No thanks.")
    $ setWait(3.88,6.966)

    $ speak(JEFFERY, "Well we're gonna get to know each other anyway, right?")
    show nicole:
        leftcenterstage
    $ setWait(6.966,15.349)
    $ speak(NICOLE, "Probably not. Probably after this week we won't even talk anymore. I've moved to a lot of different schools so I'm fully aware you're using the new kid grace period.")
    $ setWait(15.349,17.977)
    $ speak(JEFFERY, "What's \"new kid grace period\"?")
    $ setWait(17.977,23.6)
    $ speak(NICOLE, "Ugh.. it's where the outcasts squeeze all the interaction they can out of new kids way above their social status.")
    $ setWait(23.6,32.366)
    $ speak(NICOLE, "So when the new kids get here it's awkward, they don't know who's who. They'll humor any conversation or friendship until they find the people on their social level.")
    $ setWait(32.366,34.452)
    $ speak(JEFFERY, "How do you know I'm not on your social level?")
    $ setWait(34.452,38.581)
    $ speak(NICOLE, "Fucking look at you. Listen to how you talk \"How do you know I'm not\"-- shut the fuck up.")
    show jeffery angry:
        rightcenterstage
    $ setWait(38.581,40.166)
    $ speak(JEFFERY, "Hey I didn't do anything!")
    $ setWait(40.166,49.425)
    $ speak(NICOLE, "I know, it's what you will do. I've had my ear talked off about comics, laser swords, lowering the age of consent, ninja hand signs-- just all that weird shit.")
    show jeffery:
        rightcenterstage
    $ setWait(49.425,53.596)
    $ speak(JEFFERY, "You know the other pretty girls here are a lot nicer than you are.")
    $ setWait(53.596,55.89)
    $ speak(NICOLE, "They talk to you cause it's funny, get a clue.")
    $ setWait(55.89,58.017)
    $ speak(JEFFERY, "Yeah, a lot of people say I'm funny.")
    $ setWait(58.017,60.686)
    $ speak(NICOLE, "Oh you're funny? Tell me a joke.")
    $ setWait(60.686,66.15)
    $ speak(JEFFERY, "...Oh well, it's more like in the moment, you had to be there kind of funny.")
    $ setWait(66.15,69.946)
    $ speak(NICOLE, "Okay, Jeffery, you want me to save you years of guessing?")
    $ setWait(69.946,71.53)
    $ speak(JEFFERY, "Yeah sure, how?")
    $ setWait(71.53,75.952)
    $ speak(NICOLE, "They're not laughing with you, they're laughing at you cause they'll never have sex with you.")
    show jeffery happy:
        rightcenterstage
    $ setWait(75.952,81.415)
    $ speak(JEFFERY, "Ah, I got ya there! A lot of the girls here said they're saving themselves for me.")
    $ setWait(81.415,83.668)
    $ speak(NICOLE, "Christ, they make it that obvious here?")
    $ setWait(83.668,85.753)
    $ speak(JEFFERY, "Yeah they're kinda easy if you ask me.")
    $ setWait(85.753,93.511)
    show nicole angry:
        leftcenterstage
        pause 2.95
        xzoom -1
        linear 3 off_left
    $ speak(NICOLE, "No it-- ugh... Believe what you want, I'm going to lunch.")
    show jeffery:
        rightcenterstage
    $ setWait(93.511,97.014)
    $ speak(JEFFERY, "I'm funny, I know I am.")

    stop ambient fadeout 1

    jump scene_0015
label scene_0009:
    $ setVoiceTrack("audio/Scenes/0009.mp3")
    scene classroom int 2

    show nicole smile:
        leftcenterstage

    show jeffery happy:
        rightcenterstage

    $ setWait(0.106,1.758)

    $ speak(NICOLE, "I'm Nicole, hi.")
    $ setWait(1.758,3.802)

    $ speak(JEFFERY, "Huh, that's a nice name.")
    $ setWait(3.802,4.636)
    $ speak(NICOLE, "Thanks!")

    $ setWait(4.636,8.765)
    $ speak(JEFFERY, "Uh hehehe... So what animes do you like?")
    $ setWait(8.765,13.645)
    $ speak(NICOLE, "Um can't say I know too many animes, but I'd like to learn, which ones do you like?")
    show jeffery blush:
        rightcenterstage
    $ setWait(13.645,18.233)
    $ speak(JEFFERY, "Well I don't really like some of the ones other guys like...")
    $ setWait(18.233,21.736)
    $ speak(NICOLE, "Oh so you're like really into it? Really hip, you don't like the popular stuff?")
    $ setWait(21.736,32.372)
    $ speak(JEFFERY, "Mmm some are popular it's more the genre. A lot of anime is kung-fu laser beam action, I like the animes with the girls.")
    $ setWait(32.372,34.29)
    $ speak(NICOLE, "Mhm so what do like about 'em?")
    $ setWait(34.29,40.088)
    $ speak(JEFFERY, "I don't know, th-they're just really cute, I get crushes on them.")
    $ setWait(40.088,43.883)
    $ speak(NICOLE, "Oh you get crushes on cartoons? That's pretty cool.")
    show jeffery:
        rightcenterstage
    $ setWait(43.883,49.389)
    $ speak(JEFFERY, "Thanks yeah. And something else but... I should probably keep it a secret.")
    $ setWait(49.389,51.391)
    $ speak(NICOLE, "Hey hey no, come on tell me.")
    $ setWait(51.391,53.726)
    $ speak(JEFFERY, "I don't know, I just met you.")
    $ setWait(53.726,60.859)
    $ speak(NICOLE, "Here let's make a deal. You carry the load on this science lab today, and I'll keep your secret safe forever. I swear.")
    $ setWait(60.859,65.947)
    $ speak(JEFFERY, "Hm, okay that sounds like a fair deal to me. I'll tell you at lunch.")
    $ setWait(65.947,67.615)
    $ speak(NICOLE, "Cool I can't wait.")
    show jeffery happy:
        rightcenterstage
    $ setWait(67.615,71.411)
    $ speak(JEFFERY, "Now you just sit back, I'll get us an A for sure!")
    stop ambient fadeout 1
    jump scene_0016
label scene_0010:
    $ setVoiceTrack("audio/Scenes/0010.mp3")
    scene school int 2

    show nicole:
        leftcenterstage

    show kylar:
        rightcenterstage

    $ setWait(0.209,4.547)

    $ speak(NICOLE, "Like I'd love to, but I kinda make too good of decisions to get high with a stranger.")

    show kylar unhappy:
        rightcenterstage
    $ setWait(4.547,10.178)

    $ speak(KYLAR, "Aw come on don't be a pussy we fuckin' go to the same school. I'm a student athlete, people know me here.")
    $ setWait(10.178,16.225)
    $ speak(NICOLE, "Yeah \"student athlete's\" kinda the red flag here? If I pop too many I'm gonna wake up with my thighs covered in butter.")
    $ setWait(16.225,20.605)
    $ speak(KYLAR, "Bro I have done literally nothing to give you this impression of me.")
    $ setWait(20.605,24.609)
    $ speak(NICOLE, "You ever played with a sleeping teammate's ass?")
    $ setWait(24.609,27.236)
    $ speak(KYLAR, "Well... Like not in a gay way.")
    $ setWait(27.236,27.862)
    $ speak(NICOLE, "Uh huh.")
    $ setWait(27.862,28.738)
    $ speak(KYLAR, "How is that gay?")
    show nicole flipped:
        leftcenterstage
        linear 3 off_left

    $ setWait(28.738,33.785)
    $ speak(NICOLE, "Whatever I'm going to lunch. It was nice meeting you, very straight non-rapist.")
    show kylar:
        rightcenterstage
        linear 5 leftstage
    $ setWait(33.785,36.412)
    $ speak(KYLAR, "Heh yeah, makin' friends.")
    stop ambient fadeout 2
    jump scene_0017
label scene_0011:
    $ setVoiceTrack("audio/Scenes/0011.mp3")
    scene school int 2

    show nicole smile:
        leftcenterstage

    show kylar:
        rightcenterstage

    $ setWait(0.021,2.542)

    $ speak(NICOLE, "Free Percocet? Hell yeah hand it over.")
    $ setWait(2.542,8.006)

    show pills full:
        percrightcenter
        linear 0.12 xalign 0.455 yalign 0.65 rotate 345.0


    show percpop onlayer screens:
        alpha 0.0
        3
        linear .7 alpha 1.0
        2
        linear 1.5 alpha 0.0

    stop ambient fadeout 4.9

    $ speak(KYLAR, "This is actually my Mexican cartel supply but it probably won't kill ya.")

    show nicole smile:
        leftstage
    show pills full:
        xalign 0.22 yalign 0.65 rotate 345.0

    show kylar:
        leftcenterstage

    show nicole sly:
        leftstage

    $ setWait(8.006,11.926)

    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 1

    $ speak(NICOLE, "My feet feel great I could fall asleep standing right now.")


    $ setWait(11.926,13.678)

    show percpop onlayer screens:
        alpha 0.0
    $ speak(KYLAR, "Yeah I told you it was good shit.")
    $ setWait(13.678,18.808)

    show nicole:
        leftstage

    show teacher_1:
        off_right
        linear 1.7 leftcenterstage
        pause 1.85
        im.Flip("teacher_1.png", horizontal=True, vertical=False)

    show kylar unhappy:
        leftcenterstage
        pause 1.5
        linear 0.3 rightcenterstage
    show pills full:
        pause 0.35
        linear 0.09 yalign 0.7 xalign 0.28
        pause 1.15
        linear 0.2155 yalign 0.7 xalign 0.545

    $ speak(TEACHER_1, "I'm sorry are we lost? Both of you should be in class, this isn't a skip period!")
    $ setWait(18.808,22.228)

    show pills full:
        linear 0.15 yalign 0.7 xalign 0.72
        linear 0.15 yalign 0.9 xalign 0.55 rotate 30.0
        yalign 2.0 xalign 2.0
    show kylar unhappy:
        xzoom -1
        pause 0.5
        xzoom 1



    $ speak(KYLAR, "Oh fuck! Um, hey dude we were just on our way y'know?")



    show kylar unhappy:
        rightcenterstage

    hide pills full


    show teacher_1 flipped:
        linear 0.2 xalign 0.33 yalign 0.0
        pause 1.1
        linear 0.2 xalign 0.66 yalign 0.0
        linear 0.2 xalign 0.33 yalign 0.0
    show pills full:
        yalign -1.0 xalign 0.555
        pause 1.65
        yalign 0.35 xalign 0.555
        linear 0.75 yalign 2.0 xalign 0.4 rotate 270

    $ setWait(22.228,24.272)
    $ speak(TEACHER_1, "What are you hiding there?")
    $ setWait(24.272,25.231)
    $ speak(NICOLE, "Oh shit.")

    show teacher_1 angry:
        xzoom -1
        pause 1.68
        linear 0.11 xalign 0.45
        pause 1.2
        xzoom 1
        pause 1.43
        linear 0.11 leftcenterstage


    $ setWait(25.231,31.404)
    $ speak(TEACHER_1, "Prescription pills? Whose are these? Actually it doesn't matter, you're both in big trouble!")
menu:
    "PIN IT ON THE OTHER GUY":
        jump scene_0012
    "AVOID GETTING MURDERED FOR SNITCHING":
        jump scene_0013
label scene_0012:
    $ setVoiceTrack("audio/Scenes/0012.mp3")
    scene school int 2

    show nicole:
        leftstage

    show teacher_1 angry:
        leftcenterstage

    show kylar unhappy:
        rightcenterstage

    $ setWait(0.251,1.419)

    $ speak(NICOLE, "Wait wait what!?")
    show teacher_1:
        leftcenterstage
    $ setWait(1.419,2.712)

    $ speak(TEACHER_1, "Oh don't play dumb.")
    $ setWait(2.712,12.055)
    $ speak(NICOLE, "I didn't do anything, I was on my way back from the bathroom and this guy just stopped me trying to sell his.. Persoket Per- um.. I don't know but he won't leave me alone.")
    $ setWait(12.055,13.014)

    $ speak(KYLAR, "Aw come on.")

    show teacher_1 angry flipped:
        leftcenterstage
    $ setWait(13.014,16.726)
    $ speak(TEACHER_1, "Trying to find yet another customer huh, Kylar? Come with me!")
    $ setWait(16.726,19.27)
    $ speak(KYLAR, "Bro what the fuck you're seriously believing that?")

    show teacher_1 angry flipped:
        leftcenterstage
        pause 1.7
        linear 3 off_farright
    $ setWait(19.27,21.564)
    $ speak(TEACHER_1, "I don't wanna hear it, come with me!")

    show kylar unhappy:
        rightcenterstage
        linear 3.75 off_farright
    $ setWait(21.564,26.444)
    $ speak(KYLAR, "You're such a fucking bitch dude like not cool!")

    hide teacher_1
    hide kylar

    show nicole flipped:
        leftstage
        linear 2 off_left
    $ setWait(26.444,28.071)
    $ speak(NICOLE, "Oh lunchtime.")
    stop ambient fadeout 2
    jump scene_0018
label scene_0013:
    $ setVoiceTrack("audio/Scenes/0013.mp3")

    show nicole angry:
        leftstage

    show teacher_1 angry:
        leftcenterstage

    show kylar unhappy:
        rightcenterstage

    $ setWait(0.203,2.58)

    $ speak(NICOLE, "In trouble? Fuck you I'm not in anything!")
    $ setWait(2.58,5.583)

    $ speak(TEACHER_1, "Uh yeah you definitely are in trouble.")
    $ setWait(5.583,8.419)
    $ speak(NICOLE, "Well you're in the model train fan club you freak.")
    $ setWait(8.419,12.34)
    $ speak(TEACHER_1, "I'm not in the model train fan club I just sponsor the model train fan club.")
    $ setWait(12.34,13.967)
    $ speak(NICOLE, "That's even worse.")
    $ setWait(13.967,19.514)
    $ speak(TEACHER_1, "You look new here. I'm not sure what you think you're doing but I can assure you it won't last long.")
    $ setWait(19.514,22.976)
    $ speak(NICOLE, "A bitch can't pop Percs here, what the fuck? What if I had glaucoma?")
    $ setWait(22.976,29.465)
    $ speak(TEACHER_1, "But you don't have glaucoma... and you just confessed to drug use on school grounds. Come with me, both of you.")


    jump scene_0019
label scene_0014:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0


    $ setVoiceTrack("audio/Scenes/0014.mp3")

    scene cafeteria int
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1


    show nicole:
        off_left
        linear 2.6 leftcenterstage

    show jecka unhappy:
        rightcenterstage

    $ setWait(2.501,5.463)

    $ speak(JECKA, "Oh you look new, the lunch line's on the other end there.")
    $ setWait(5.463,6.339)

    $ speak(NICOLE, "Huh?")
    $ setWait(6.339,12.219)
    $ speak(JECKA, "You're trying to find where the lunch line starts, right? You got here a little late so it's pretty long now.")
    $ setWait(12.219,15.64)
    $ speak(NICOLE, "Oh! Fuck for a sec I thought everyone else was skipping too.")
    $ setWait(15.64,17.266)
    $ speak(JECKA, "Where'd you come in from?")
    $ setWait(17.266,21.103)
    $ speak(NICOLE, "Like just outside. There was this weird kid getting his shit handed to him.")
    $ setWait(21.103,22.647)
    $ speak(JECKA, "Like weird how?")
    $ setWait(22.647,23.856)
    $ speak(NICOLE, "I don't fuckin' know.")
    $ setWait(23.856,30.655)
    $ speak(JECKA, "Is he like \"talks about a bunch of dumb shit\" weird? Or like \"how can he afford so much adderall with a job at the Shop 'n Save\" weird?")
    $ setWait(30.655,32.615)
    $ speak(NICOLE, "Um... first one.")
    $ setWait(32.615,42.124)
    $ speak(JECKA, "Oh, glasses, bowl cut, that's Jeffery. I don't think he's all there. Like he's too socially awkward for the normal people but too smart for the special eddies.")
    $ setWait(42.124,43.125)
    $ speak(NICOLE, "Can I sit here?")
    $ setWait(43.125,46.671)
    $ speak(JECKA, "Yeah sure, all my friends got put in a different lunch period.")
    $ setWait(46.671,48.506)
    $ speak(NICOLE, "What's your name? I'm Nicole.")
    $ setWait(48.506,49.757)
    $ speak(JECKA, "I'm Jecka.")
    $ setWait(49.757,52.718)
    $ speak(NICOLE, "Jecka? That's like on your birth certificate?")
    $ setWait(52.718,54.428)
    $ speak(JECKA, "Short for Jessica, obvi.")
    $ setWait(54.428,57.974)
    $ speak(NICOLE, "That's pretty punk for someone who dresses so...")
    show jecka:
        rightcenterstage
    $ setWait(57.974,65.439)
    $ speak(JECKA, "Preppy? Yeah my Mom works corporate for department stores so I get all this expensive stuff for free but trust me, I don't give a fuck.")
    show nicole smile:
        leftcenterstage
    $ setWait(65.439,67.024)
    $ speak(NICOLE, "Cool yeah same.")

    stop ambient fadeout 1

    jump scene_0023
label scene_0015:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0


    $ setVoiceTrack("audio/Scenes/0015.mp3")
    scene cafeteria int
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1

    show nicole:
        leftstage

    $ setWait(0.67,4.174)

    $ speak(NICOLE, "God the food here is tragic. Even the air has preservatives.")

    show jecka unhappy:
        off_right
        linear 1.6 rightcenterstage
    $ setWait(4.174,6.509)

    $ speak(JECKA, "Fucking tell me about it, that's why I pack.")


    $ setWait(6.509,8.136)
    $ speak(NICOLE, "Oh sorry, didn't see you.")
    $ setWait(8.136,12.015)
    $ speak(JECKA, "Nah it's okay you can sit here. I'm Jecka, where you in from?")

    show nicole:
        leftstage
        linear 1 leftcenterstage

    $ setWait(12.015,16.227)
    $ speak(NICOLE, "Uh Chemistry? I think, I don't know I didn't really do anything.")
    $ setWait(16.227,20.315)
    $ speak(JECKA, "Aw that sucks yeah you have to like wash acid off you before you can touch your food.")
    $ setWait(20.315,27.572)
    $ speak(NICOLE, "I'm not eating anyway. The guy I had to sit next to scared my appetite away... pretty much just me away in general.")
    $ setWait(27.572,29.657)
    $ speak(JECKA, "Who was it? Do you know?")
    $ setWait(29.657,31.242)
    $ speak(NICOLE, "Um, Jeffery?")
    $ setWait(31.242,33.411)
    $ speak(JECKA, "Ohhh yep, he's a fun one.")
    $ setWait(33.411,36.372)
    $ speak(NICOLE, "But he's so like overly chummy, that's fun to you?")
    $ setWait(36.372,45.757)
    $ speak(JECKA, "No like fun to fuck with him, duh. Freshman year every girl put love notes on his locker, right? So he went up to some of the girls' boyfriends like \"ha she's in love with me now\"")
    $ setWait(45.757,47.759)
    $ speak(NICOLE, "Oh my god, that's funny.")
    $ setWait(47.759,54.39)
    $ speak(JECKA, "But cause they were all like 14, three guys just beat the shit out of him for it. Now we have all these stupid anti-bullying rules.")
    $ setWait(54.39,56.893)
    $ speak(NICOLE, "I never got how they could like enforce that?")
    $ setWait(56.893,61.189)
    $ speak(JECKA, "It's baby simple, if you don't wanna get bullied just be hot and sociable.")
    $ setWait(61.189,64.776)
    $ speak(NICOLE, "Fucking accurate... I'm Nicole by the way.")
    $ setWait(64.776,67.445)
    $ speak(JECKA, "Well I'll see you around, Nicole.")

    stop ambient fadeout 1

    jump scene_0023
label scene_0016:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0


    $ setVoiceTrack("audio/Scenes/0016.mp3")
    scene cafeteria int 2
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1

    show nicole smile:
        leftcenterstage

    show jeffery happy:
        rightcenterstage

    $ setWait(0.498,4.043)

    $ speak(NICOLE, "You did such a good job, I'm almost jealous actually.")
    $ setWait(4.043,7.755)

    $ speak(JEFFERY, "Aw there's nothing to it, I could tutor you after school or something.")
    $ setWait(7.755,11.759)
    $ speak(NICOLE, "Mmm we'll worry about that later, so what were you gonna tell me in class?")
    $ setWait(11.759,15.262)
    $ speak(JEFFERY, "Oh about how nail polish remover can melt styrofoam.")
    show nicole sly:
        leftcenterstage

    show jeffery:
        rightcenterstage
    $ setWait(15.262,19.266)
    $ speak(NICOLE, "No before that... the girls in your favorite animes?")
    show jeffery blush:
        rightcenterstage
    $ setWait(19.266,28.442)
    $ speak(JEFFERY, "Oh yeah um... well I think they're really really cute... but sometimes more than cute?")
    $ setWait(28.442,31.612)
    $ speak(NICOLE, "Like... like all the way?")
    $ setWait(31.612,40.746)
    $ speak(JEFFERY, "Um, well a promise is a promise... I think some of them are very sexy.")
    $ setWait(40.746,42.54)
    $ speak(NICOLE, "Oh, you like 'em that way, huh?")
    $ setWait(42.54,47.044)
    $ speak(JEFFERY, "Yeah cause their bodies are just so... perfect.")
    $ setWait(47.044,50.923)
    $ speak(NICOLE, "Uh huh totally. They are drawn so perfect.")
    $ setWait(50.923,53.634)
    $ speak(JEFFERY, "Y-you don't think that's weird, right?")
    $ setWait(53.634,57.972)
    $ speak(NICOLE, "No it's perfectly normal... I think, can't really check right now.")
    $ setWait(57.972,68.733)
    $ speak(JEFFERY, "Thanks. And sometimes when I'm... pent up I... pause the anime at certain frames and I... y'know?")
    $ setWait(68.733,71.318)
    $ speak(NICOLE, "No I don't know, tell me.")
    $ setWait(71.318,77.408)
    $ speak(JEFFERY, "I kinda like.. y'know, use my hand.")
    show nicole:
        leftcenterstage
    $ setWait(77.408,81.412)
    $ speak(NICOLE, "Oh.. like to completion?")
    $ setWait(81.412,82.747)
    $ speak(JEFFERY, "Yeah...")
    show nicole smile:
        leftcenterstage
    $ setWait(82.747,85.75)
    $ speak(NICOLE, "I think that's awesome, it's so great that you do that.")
    $ setWait(85.75,94.008)
    $ speak(JEFFERY, "Oh thanks... you're the first girl I ever told that to. I like you, Nicole. Can we talk tomorrow?")
    show nicole smile:
        leftcenterstage
    $ setWait(94.008,97.428)
    $ speak(NICOLE, "...Yeah, fuck it. Hey tonight, tell those girls I said hi.")
    show jeffery happy:
        rightcenterstage
    $ setWait(97.428,101.112)
    $ speak(JEFFERY, "Okay, anything for you, Nicole.")

    stop ambient fadeout 2

    jump scene_0025
label scene_0017:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0


    $ setVoiceTrack("audio/Scenes/0017.mp3")
    scene cafeteria int
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1

    show jecka flipped:
        rightstage

    show nicole angry:
        off_left
        linear 1.5 leftcenterstage

    $ setWait(0.496,3.499)

    $ speak(NICOLE, "God damn this school's nothing but rapists and pedophiles.")

    show jecka unhappy:
        rightstage
        linear 0.6 rightcenterstage

    $ setWait(3.499,4.834)

    $ speak(JECKA, "Tell me about it.")
    $ setWait(4.834,7.753)
    $ speak(NICOLE, "Oh sorry, if you're sitting here I can go somewhere else.")
    $ setWait(7.753,10.256)
    $ speak(JECKA, "Nah I don't think anyone's showing up, go ahead.")
    $ setWait(10.256,12.174)
    $ speak(NICOLE, "Thanks. What's your name?")
    $ setWait(12.174,22.059)
    $ speak(JECKA, "Jecka. Now before I ask your name, I just wanna ask what happened to you. Like it took me 2 years to figure out this school sucks, you did it on your first day, what's up?")
    $ setWait(22.059,24.228)
    $ speak(NICOLE, "...A lacrosse player wanted me to get high.")
    $ setWait(24.228,27.189)
    $ speak(JECKA, "Like Benadryl or a prescription high?")
    $ setWait(27.189,28.774)
    $ speak(NICOLE, "Full on Percocet, dude.")
    $ setWait(28.774,35.114)
    $ speak(JECKA, "Oh that's um... fuck what was his name? Kylar yeah! Yeah he's a bit of a benzosexual.")
    $ setWait(35.114,37.408)
    $ speak(NICOLE, "What the fuck's a benzosexual?")
    $ setWait(37.408,39.827)
    $ speak(JECKA, "Attracted to the unconscious.")
    $ setWait(39.827,43.164)
    $ speak(NICOLE, "Oh... well hi I'm Nicole I just dodged a bullet.")
    $ setWait(43.164,49.336)
    $ speak(JECKA, "Cool hey. Um, so the other guys you gotta watch out for are usually into some form of feet.")

    stop ambient fadeout 1
    jump scene_0023
label scene_0018:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0018.mp3")
    scene cafeteria int 2
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1

    show jecka unhappy:
        rightstage

    show nicole sly:
        off_left
        linear 3.2 leftcenterstage

    $ setWait(0.702,3.789)

    $ speak(NICOLE, "That was the ultimate win-win...")

    show jecka unhappy:
        rightstage
        linear 0.65 rightcenterstage
    $ setWait(3.789,6.375)

    $ speak(JECKA, "Hey uh, are you okay?")

    show nicole sly:
        leftcenterstage

    $ setWait(6.375,12.672)
    $ speak(NICOLE, "What? --Oh no I'm good as shit, dude. I don't feel great, just nice.")
    $ setWait(12.672,15.967)
    $ speak(JECKA, "So is anyone else gonna be sitting here or?")
    $ setWait(15.967,19.721)
    $ speak(NICOLE, "Oh sit here all you want, I'm new here I have no say.")
    $ setWait(19.721,24.643)
    $ speak(JECKA, "Cool thanks... Um, I'm just gonna say it, are you fucked up?")
    $ setWait(24.643,25.727)
    $ speak(NICOLE, "Are you?")
    $ setWait(25.727,27.938)
    $ speak(JECKA, "Emotionally, absolutely.")
    $ setWait(27.938,31.525)
    $ speak(NICOLE, "I'm not rich enough to turn down free Percocet.")
    $ setWait(31.525,36.196)
    $ speak(JECKA, "Yeah that lacrosse guy loves the new girls. Did you pocket any, can I have one?")
    $ setWait(36.196,40.409)
    $ speak(NICOLE, "No it got broken up real quick, a teacher caught us and I just pinned it on him.")
    show jecka:
        rightcenterstage
    $ setWait(40.409,43.078)
    $ speak(JECKA, "That's fucking bad ass, what's your name?")
    $ setWait(43.078,47.707)
    $ speak(NICOLE, "I'm Nicole, but don't say that really loud I don't want these people to know me.")
    $ setWait(47.707,51.878)
    $ speak(JECKA, "Don't worry, I know... So what electives are you taking?")
    $ setWait(51.878,56.133)
    $ speak(NICOLE, "Like uh.. is English an elective?")
    $ setWait(56.133,58.218)
    $ speak(JECKA, "It should be, but no.")
    $ setWait(58.218,60.512)
    $ speak(NICOLE, "Okay then it was photography.")
    $ setWait(60.512,63.807)
    $ speak(JECKA, "Me too, We might be in the same class!")
    show nicole:
        leftcenterstage
    $ setWait(63.807,67.519)
    $ speak(NICOLE, "If you'd.. like to get that excited about it-- yeah we might be.")
    $ setWait(67.519,69.187)
    $ speak(JECKA, "Oh you're too cool for school?")
    $ setWait(69.187,75.152)
    $ speak(NICOLE, "Well no, right now I feel warm as hell, have you popped perc? It's a blanket in a pill.")
    $ setWait(75.152,78.155)
    $ speak(JECKA, "Yeah I've popped perc, how the fuck is it a blanket in a pill?")
    $ setWait(78.155,82.367)
    $ speak(NICOLE, "It turns off all the coldness sensors, you just feel nice and cozy.")
    $ setWait(82.367,83.91)
    $ speak(JECKA, "You're fun.")



    stop ambient fadeout 1
    jump scene_0023
label scene_0019:
    $ setVoiceTrack("audio/Scenes/0019.mp3")
    play ambient "audio/Ambience/Neighborhood_Ambience_Night.mp3" fadein 1
    scene onlayer master
    show black
    show home nicole ext night with Pause(2.038):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.038 zoom .6 truecenter



    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3"

    show nicole shirt angry:
        leftcenterstage

    show mom:
        rightstage
        linear 4.2 rightcenterstage

    $ setWait(2.038,7.794)
    $ speak(MOM, "Honey... what the fuck is wrong with you? A 2-day suspension on the first day of school?")
    $ setWait(7.794,12.381)
    $ speak(NICOLE, "It was like one pill, he's just mad I made him feel insecure so he threw the book at me!")
    $ setWait(12.381,15.092)
    $ speak(MOM, "Look I know you're acting out because of your father--")
    $ setWait(15.092,19.8)
    $ speak(NICOLE, "Mom, literally no one ever has actively thought \"I'm gonna act out today!\" What does that even mean?")
    $ setWait(19.8,24.602)
    $ speak(NICOLE, "\"I'm gonna look cool by disrespecting my parents!\" this is a world you and everyone who crochets created.")
    show gamer_brother:
        off_right
        linear 2.0 rightstage

    $ setWait(24.602,26.521)
    $ speak(GAMER_BROTHER, "She kinda has a point with that, Mom.")

    show mom flipped:
        rightcenterstage
    $ setWait(26.521,29.19)
    $ speak(MOM, "You kinda need to get a fucking job, you're 26.")
    $ setWait(29.19,35.822)
    $ speak(GAMER_BROTHER, "I told you the economy's bad, blame Bush! And these girls I chat with online fully agree!")
    $ setWait(35.822,41.953)
    $ speak(NICOLE, "Mom, still, I can't believe you're taking the school's side with this. It's totally against all my citizen rights!")
    show mom:
        rightcenterstage
    $ setWait(41.953,46.999)
    $ speak(MOM, "They had you sign something that waives those rights-- you're 16 you don't even have rights.")
    $ setWait(46.999,50.086)
    $ speak(NICOLE, "Well you do, right? Sue the school or something!")
    show mom angry:
        rightcenterstage
    $ setWait(50.086,59.47)
    $ speak(MOM, "You're at the only public school for miles and miles. What happens if you're gone for good, huh? I'm not moving again, I'm not paying for private school, and I'm definitely not homeschooling.")

    show gamer_brother flipped:
        rightstage
        linear 3.6 off_farright

    $ setWait(59.47,66.811)
    $ speak(NICOLE, "Fine I won't blow it then, I won't squeal a bit. A teacher could just rape the shit out of me but I won't say a word cause we gotta stay in this shit hole!")
    $ setWait(66.811,69.146)
    $ speak(MOM, "Good, I'm glad we understand each other.")
    $ setWait(69.146,71.899)
    $ speak(NICOLE, "Mom! I could just get assaulted, you wouldn't care?")
    $ setWait(71.899,76.32)
    $ speak(MOM, "You've been pulling the sexual assault card since you were 12, hasn't happened yet, has it?")
    $ setWait(76.32,78.155)
    $ speak(NICOLE, "That's not the fucking point!")
    $ setWait(78.155,82.66)
    $ speak(MOM, "Well you can figure out a new excuse locked in your bedroom for the next 2 days.")

    show nicole shirt angry flipped:
        leftcenterstage
        linear 3.5 off_left
    $ setWait(82.66,86.497)
    $ speak(NICOLE, "Fine! I have my own computer, grounding doesn't do shit anymore.")

    stop ambient fadeout 1
    jump scene_0020
label scene_0020:

    show black onlayer screens with Pause(1):
        alpha 0.0
        linear 1 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 0.7 alpha 0.0


    $ setVoiceTrack("audio/Scenes/0020.mp3")
    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3" fadein 1

    show gamer_brother flipped:
        rightcenterstage

    $ setWait(1.095,6.976)

    $ speak(GAMER_BROTHER, "Yeah baby you hear this!? This is some real music! Now join my party chat and we can game!")

    show nicole tanktop angry:
        off_left
        linear 3 leftcenterstage

    show gamer_brother:
        rightcenterstage

    $ setWait(6.976,10.647)
    $ speak(NICOLE, "What the fuck are you doing? It's 1am I go back to school tomorrow!")
    $ setWait(10.647,13.816)
    $ speak(GAMER_BROTHER, "Bro you're being seriously fail right now.")
    $ setWait(13.816,17.779)
    $ speak(NICOLE, "\"Seriously fail\".. those words don't even go together you sound like an idiot.")
    $ setWait(17.779,23.409)
    $ speak(GAMER_BROTHER, "Look I'm just recording a little voice message for this hottie I met online then I'm done okay?")
    $ setWait(23.409,27.914)
    $ speak(NICOLE, "This is like the 5th \"hottie\" in 2 days. Do you know how old any of these girls are?")
    $ setWait(27.914,31.125)
    $ speak(GAMER_BROTHER, "Like, legal in her country don't worry about it.")
    show nicole tanktop sad:
        leftcenterstage
    $ setWait(31.125,32.877)
    $ speak(NICOLE, "Oh my god, this is bad.")
    $ setWait(32.877,37.423)
    $ speak(GAMER_BROTHER, "I'm just trying to score some 15-year old Canadian ass, hop off it.")

    show nicole angry tanktop:
        leftcenterstage
    $ setWait(37.423,41.761)
    $ speak(NICOLE, "15 isn't legal anywhere, calling her Canadian ass doesn't make that better.")
    $ setWait(41.761,49.852)
    $ speak(GAMER_BROTHER, "Well no, y'know how like Canadian bacon is just ham? Canadian ass is just a mature 15 year old. See? Same thing.")


    $ setWait(49.852,52.105)
    $ speak(NICOLE, "You're.. Oh my god..")
    $ setWait(52.105,55.984)
    $ speak(GAMER_BROTHER, "Could you just help me record this message so we can both go to bed quicker?")
menu:
    "DISTRACT HIM INTO DOING SOMETHING ELSE":
        jump scene_0021
    "MAKE HIM GONE FOR GOOD":
        jump scene_0022
label scene_0021:
    $ setVoiceTrack("audio/Scenes/0021.mp3")
    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3"

    show nicole tanktop:
        leftcenterstage

    show gamer_brother:
        rightcenterstage

    $ setWait(0.039,6.846)

    $ speak(NICOLE, "Hey um.. did you get that new shooter game? The one where you're a white guy shooting brown people in a non-racist way?")
    $ setWait(6.846,13.227)

    $ speak(GAMER_BROTHER, "Oh Warfare? Yeah hell yeah I got it. Had to steal out of Mom's purse but it's get paid or get played, y'know what I mean?")
    $ setWait(13.227,17.106)
    $ speak(NICOLE, "Uh yeah I guess. Can I play with you?")
    $ setWait(17.106,19.776)
    $ speak(GAMER_BROTHER, "I thought you didn't like video games anymore.")
    $ setWait(19.776,22.987)
    $ speak(NICOLE, "I started using an anti-aging cream so my hobbies should match my skin.")

    show gamer_brother flipped:
        rightcenterstage
        linear 6.6 off_farright

    $ setWait(22.987,26.324)
    $ speak(GAMER_BROTHER, "Works for me, but you're player 2, bitch.")

    show nicole tanktop:
        leftcenterstage
        linear 6 off_right

    $ setWait(26.324,29.076)
    $ speak(NICOLE, "How could any adult woman not like video games?")

    stop ambient fadeout 1
    jump scene_0024
label scene_0022:
    $ setVoiceTrack("audio/Scenes/0022.mp3")
    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3"

    show nicole tanktop sly:
        leftcenterstage

    show gamer_brother:
        rightcenterstage

    $ setWait(0.113,4.717)
    $ speak(NICOLE, "What's the point? Whatever girl you're hitting up's probably ugly compared to what I could find.")

    $ setWait(4.717,7.678)
    $ speak(GAMER_BROTHER, "You haven't even seen her avatar she's like so hot.")

    $ setWait(7.678,10.64)
    $ speak(NICOLE, "Where are you logged in at? I bet I could find a better one.")

    show black onlayer screens:
        alpha 0.0
        linear 1.5 alpha 1.0
        1.7
        linear 0.88 alpha 0.0

    stop ambient fadeout 1.6
    $ setWait(10.64,13.684)
    $ speak(GAMER_BROTHER, "You're on.")

    play ambient "audio/Ambience/House_Night_Ambience.mp3" fadein 1

    show nicole tanktop smile:
        leftcenterstage

    $ setWait(13.684,22.818)
    $ speak(NICOLE, "See? This girl right here. KinkyKenzie93, her bio's like \"only interested in older guys so hit me up whenever, up for anything\".")

    show black onlayer screens:
        alpha 0.0
    $ setWait(22.818,24.487)
    $ speak(GAMER_BROTHER, "Man she's sexy.")

    show nicole tanktop:
        leftcenterstage

    $ setWait(24.487,25.821)
    $ speak(NICOLE, "She's also 14.")

    show gamer_brother upset:
        rightcenterstage

    $ setWait(25.821,32.495)
    $ speak(GAMER_BROTHER, "Shut up with that ageist, bullshit. Oh man she's just a town over too, I'm gonna message her what should I say?")

    $ setWait(32.495,35.289)
    $ speak(NICOLE, "You're like a legal adult, shouldn't you know how to do this by now?")

    $ setWait(35.289,39.335)
    $ speak(GAMER_BROTHER, "Yeah but you're a girl, you know what girls wanna hear, come on.")

    $ setWait(39.335,46.759)
    $ speak(NICOLE, "Alright fine. Um, first tell her you're 26. Girls who like older men are all about that age difference.")

    $ setWait(46.759,48.052)
    $ speak(GAMER_BROTHER, "Okay, what else?")

    $ setWait(48.052,52.556)
    $ speak(NICOLE, "Say you wanna buy her drugs and alcohol, and no pussy shit. Like full on heroin.")

    $ setWait(52.556,58.771)
    $ speak(GAMER_BROTHER, "I'm sure other guys promised that too though, right? When guys hit you up, what do they never do?")

    $ setWait(58.771,64.527)
    $ speak(NICOLE, "Hmm.. Oh! At the bottom, type an acrostic poem using your driver's license number.")

    $ setWait(64.527,65.903)
    $ speak(GAMER_BROTHER, "I don't know...")

    $ setWait(65.903,70.032)
    $ speak(NICOLE, "But like, have the message of the poem be about how you don't wanna use a condom.")

    show black onlayer screens:
        alpha 0.0
        3.2
        linear 1.5 alpha 1.0
        7.4
        linear 0.15 alpha 0.0

    stop ambient fadeout 6.5

    show gamer_brother:
        rightcenterstage

    $ setWait(70.032,82.044)
    $ speak(GAMER_BROTHER, "Dude! ...That's like genius! She's gonna so want the D.")

    hide nicole

    show gamer_brother upset flipped:
        off_left
        linear 0.3 leftcenterstage

    show cop:
        off_right
        linear 0.6 rightstage

    play ambient "audio/Ambience/House_Night_Ambience.mp3" fadein 0.3
    $ setWait(82.044,84.046)
    $ speak(GAMER_BROTHER, "Whoa what do you want!?")

    show black onlayer screens:
        alpha 0.0

    $ setWait(84.046,86.882)
    $ speak(COP, "Are you dating site user \"Heavy D no MC\"?")

    $ setWait(86.882,92.847)
    $ speak(GAMER_BROTHER, "Yeah but I don't know what that has to do with you busting in here! By the way that's like a sick user name, right--")

    show cop:
        rightstage
        linear 0.2 rightcenterstage

    show gamer_brother upset flipped:
        leftcenterstage
        pause 1
        linear 0.6 leftstage
    $ setWait(92.847,96.6)
    $ speak(COP, "You're under arrest for digital misconduct with a minor!")

    show cop:
        rightcenterstage

    show gamer_brother upset flipped:
        leftstage
        linear 0.8 leftcenterstage

    $ setWait(96.6,99.812)
    $ speak(GAMER_BROTHER, "Aw that Kenzie bitch snitched me out, god dammit!")

    show cop:
        rightcenterstage
        pause 6.1
        linear 0.1 xalign 0.5

    show gamer_brother upset flipped:
        leftcenterstage
    $ setWait(99.812,106.527)
    $ speak(COP, "Rest assured, there was no Kenzie. We can talk all about how you fell for a sting operation downtown!")

    show gamer_brother upset:
        leftcenterstage
        linear 7 off_farright


    show cop:
        xalign 0.5
        linear 6 off_farright
    $ setWait(106.527,114.869)
    $ speak(GAMER_BROTHER, "I was set up! Fuckin' Nicole you bitch, my first phone call's gonna be a bomb threat to your friends!")
    stop ambient fadeout 1

    jump scene_0024
label scene_0023:



    show black onlayer screens with Pause(1.5):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.2 alpha 0.0

    scene school ext 1
    $ setVoiceTrack("audio/Scenes/0023.mp3")
    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 1

    show jecka sc2:
        rightstage
        linear 1.25 rightcenterstage

    show nicole sc2:
        off_left
        linear 3.7 leftcenterstage
    $ setWait(0.625,3.461)
    $ speak(JECKA, "Nicole! You ready for day 2?")
    $ setWait(3.461,6.881)
    $ speak(NICOLE, "Is someone gonna kill me day 2? If so, absolutely.")
    show jecka sc2 unhappy:
        rightcenterstage
    $ setWait(6.881,8.591)
    $ speak(JECKA, "Why? What happened?")
    $ setWait(8.591,16.141)
    $ speak(NICOLE, "Just like waking up in general hurts. And I gotta deal with my brother who's still up from the night before eating a family-box of anything.")
    $ setWait(16.141,19.269)
    $ speak(JECKA, "He can eat family sized meals? How old is he?")
    $ setWait(19.269,22.772)
    $ speak(NICOLE, "Like 26, he just freeloads off my Mom.")
    $ setWait(22.772,26.651)
    $ speak(JECKA, "I mean we kinda freeload too but we're 16, it's cool when we do it.")
    $ setWait(26.651,31.031)
    $ speak(NICOLE, "Exactly, I have to tell him that when I'm woken up by loud chewing noises.")
    $ setWait(31.031,32.615)
    $ speak(JECKA, "Is he fat?")
    $ setWait(32.615,35.285)
    $ speak(NICOLE, "Do you know what \"ex-bodybuilder fat\" is?")
    $ setWait(35.285,37.62)
    $ speak(JECKA, "Yeah I kinda know what that looks like.")
    $ setWait(37.62,43.543)
    $ speak(NICOLE, "Well he's an obese monster. I was just curious if anyone else knew that bodybuilder phrase-- he's not that.")
    $ setWait(43.543,46.921)
    $ speak(JECKA, "Good to know. Hey let's gossip more at lunch, I gotta get to class.")
    $ setWait(46.921,48.84)
    $ speak(NICOLE, "Dude fuck class just skip with me.")
    $ setWait(48.84,54.054)
    $ speak(JECKA, "I told you yesterday, if I skip any more my Mom's gonna start giving me disciplinary tattoos.")
    $ setWait(54.054,56.347)
    $ speak(NICOLE, "How does that even work? What does she write on you?")
    $ setWait(56.347,60.602)
    $ speak(JECKA, "It'd be some weird shit like \"I LOVE SCHOOL\" on my fingers.")
    $ setWait(60.602,63.188)
    $ speak(NICOLE, "Isn't that like... abusive?")
    $ setWait(63.188,66.858)
    $ speak(JECKA, "She's the only Mom I've ever had, how the fuck should I know?")
    $ setWait(66.858,68.193)
    $ speak(NICOLE, "...Huh.")
    $ setWait(68.193,69.694)
    $ speak(JECKA, "So where you headed?")

    stop ambient fadeout 2
    menu:
        "GYM CLASS":
            jump scene_0026
        "PHOTOGRAPHY":
            jump scene_0027
label scene_0024:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0024.mp3")
    scene school ext 2
    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 2

    show nicole sc2:
        off_left
        linear 6 leftcenterstage

    show crispin sc2:
        xzoom -1
        rightstage

    $ setWait(1.007,8.306)
    $ speak(NICOLE, "My big mistake wasn't getting suspended, but getting suspended on the first day before meeting anyone. Now I can't look badass when I come back.")

    show crispin sc2:
        xzoom 1
        rightstage
        linear 1.5 rightcenterstage

    show jecka sc2:
        off_right
        pause 1.5
        linear 2 rightstage

    show nicole sc2:
        leftcenterstage

    $ setWait(8.306,10.975)
    $ speak(CRISPIN, "Hey what's up? Haven't seen you around for a couple days.")

    show crispin sc2 unhappy:
        rightcenterstage
        pause 2
        xzoom -1
        linear 4 off_right

    $ setWait(10.975,14.437)
    $ speak(NICOLE, "Fuck off and die.")

    show jecka sc2 unhappy:
        rightstage
        linear 1.6 rightcenterstage


    $ setWait(14.437,18.441)
    $ speak(JECKA, "Hey you.. don't look familiar at all, are you new here?")

    hide crispin
    $ setWait(18.441,21.486)
    $ speak(NICOLE, "Kinda, I'm back from a 2-day suspension.")
    $ setWait(21.486,23.529)
    $ speak(JECKA, "It's the 3rd day of school...")
    $ setWait(23.529,24.948)
    $ speak(NICOLE, "I don't beat around the bush.")
    show jecka sc2:
        rightcenterstage
    $ setWait(24.948,26.95)
    $ speak(JECKA, "You're cool as shit, what's your name?")
    $ setWait(26.95,27.951)
    $ speak(NICOLE, "Call me Nicole.")
    $ setWait(27.951,30.995)
    $ speak(JECKA, "Hey I'm Jecka. So how do you know Crispin?")
    $ setWait(30.995,32.205)
    $ speak(NICOLE, "Who's Crispin?")
    $ setWait(32.205,33.957)
    $ speak(JECKA, "That guy you were just talking to?")
    $ setWait(33.957,39.796)
    $ speak(NICOLE, "Oh, guitar pick necklace? Both days I've been here he's tried talking to me, I have no idea who he is.")
    $ setWait(39.796,44.425)
    $ speak(JECKA, "He's kinda nice. I wouldn't be surprised if he burned down a convenience store but yeah he's nice.")
    $ setWait(44.425,48.429)
    $ speak(NICOLE, "I'll tolerate just about anyone after being locked up with my brother for 2 days.")
    show jecka sc2:
        rightcenterstage
    $ setWait(48.429,52.392)
    $ speak(JECKA, "Oh is he younger? Into really loud, violent video games?")
    $ setWait(52.392,56.854)
    $ speak(NICOLE, "Close! He's 26 and into really loud, violent video games.")
    $ setWait(56.854,59.148)
    $ speak(JECKA, "Oh that's tragic, he lives at home still?")
    $ setWait(59.148,62.276)
    $ speak(NICOLE, "Yeah. He's never even attempted couch surfing.")
    $ setWait(62.276,65.154)
    $ speak(JECKA, "Can't he get like a boyfriend to live off or something?")
    $ setWait(65.154,68.074)
    $ speak(NICOLE, "No, he's not gay... at least not that kind.")
    $ setWait(68.074,71.828)
    $ speak(JECKA, "Then can't he like... turn gay and get a boyfriend to live off?")
    $ setWait(71.828,78.459)
    $ speak(NICOLE, "Fucked up, I asked that exact same question and all he said was \"bottoms don't top FPS leaderboards\".")
    $ setWait(78.459,85.341)
    $ speak(JECKA, "Oh so he's like... really into video games. Is he one of those guys that like end up on the news for messaging kids?")
    $ setWait(85.341,88.72)
    $ speak(NICOLE, "Last night he begged a 15 year old for naked pictures.")
    $ setWait(88.72,92.348)
    $ speak(JECKA, "Oh my god, he's that guy. Is he in prison yet?")
    $ setWait(92.348,94.142)
    $ speak(NICOLE, "Uh... we'll see.")
    $ setWait(94.142,99.272)
    $ speak(JECKA, "Hey I'd love to hang around more but I gotta get to class. Where are you headed to?")

    stop ambient fadeout 2

    menu:
        "GYM CLASS":
            jump scene_0026
        "PHOTOGRAPHY":
            jump scene_0027
label scene_0025:

    show black onlayer screens with Pause(2.8):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1
        linear 2 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0025.mp3")
    scene school ext 2
    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 2

    show jecka sc2 unhappy:
        rightcenterstage

    show nicole sc2:
        off_left
        linear 3.2 leftcenterstage

    $ setWait(0.752,5.715)
    $ speak(NICOLE, "Hey sorry, but we do have to go to a homeroom first? Or do we just go straight to first period?")

    show nicole sc2:
        leftcenterstage

    $ setWait(5.715,10.428)
    $ speak(JECKA, "No it's okay, yeah first period. There's no homeroom here. You're new?")
    $ setWait(10.428,16.601)
    $ speak(NICOLE, "Yeah it's my second day. I wish all schools were just built the same so it wouldn't be a learning curve every time I moved.")
    $ setWait(16.601,18.311)
    $ speak(JECKA, "Oh are you a military kid?")
    $ setWait(18.311,22.357)
    $ speak(NICOLE, "If ho'ing's a battlefield then yes. My Mom divorces and moves a lot.")
    $ setWait(22.357,24.442)
    $ speak(JECKA, "Well how do you think all schools should be built?")
    $ setWait(24.442,31.699)
    $ speak(NICOLE, "Geometrically all the same with universal room numbering. Oh and make them all just one floor. Two flights is confusing.")
    show jecka sc2:
        rightcenterstage
    $ setWait(31.699,34.786)
    $ speak(JECKA, "But then how are we gonna push fat kids down the stairs?")
    $ setWait(34.786,36.496)
    $ speak(NICOLE, "Fuck you're right, what's your name?")
    $ setWait(36.496,38.039)
    $ speak(JECKA, "Jecka, what's yours?")
    $ setWait(38.039,40.833)
    $ speak(NICOLE, "Nicole. Why'd your parents name you Jecka?")
    show jecka sc2 unhappy:
        rightcenterstage
    $ setWait(40.833,48.174)
    $ speak(JECKA, "Well no they called me \"Jessica\" but I started doing Jecka for short. Also Jessica's a name that just screams: \"married at 20\".")
    $ setWait(48.174,50.635)
    $ speak(NICOLE, "Oh yeah marriage sucks, never doing it.")
    $ setWait(50.635,51.552)
    $ speak(JECKA, "Totally.")
    show jeffery sc2:
        xzoom -1
        off_left
        pause 2
        linear 3 leftstage

    $ setWait(51.552,55.431)
    $ speak(NICOLE, "Whenever I play Fuck-Marry-Kill I answer \"Fuck Marriage and Kill myself\".")

    show nicole sc2 surprised:
        pause 0.5
        xzoom -1
        leftcenterstage

    $ setWait(55.431,57.475)
    $ speak(JEFFERY, "Hey Nicole, how ya doing?")

    show jeffery sc2 happy:
        leftstage

    $ setWait(57.475,58.893)
    $ speak(NICOLE, "Oh fuck I forgot.")
    $ setWait(58.893,60.144)
    $ speak(JECKA, "Do you know each other?")

    show nicole sc2 smile:
        xzoom 1
        leftcenterstage

    $ setWait(60.144,61.062)
    $ speak(NICOLE, "No not really--")
    show nicole sc2:
        leftcenterstage
    $ setWait(61.062,67.735)
    $ speak(JEFFERY, "'Course we do! I met Nicole yesterday in science class, then we had lunch together and talked about anime!")

    show jecka sc2 worried:
        rightcenterstage
        pause 1.5
        linear 1.5 rightstage

    $ setWait(67.735,71.114)
    $ speak(JECKA, "Wow Nicole you're kinda.. less cool now.")
    show nicole sc2 surprised:
        leftcenterstage
    $ setWait(71.114,73.533)
    $ speak(NICOLE, "What? No! He's just making shit up!")


    $ setWait(73.533,77.412)
    $ speak(JECKA, "Anyway I gotta get to class now, I'll leave you two to your anime talk.")

    show jecka sc2 unhappy:
        xzoom -1
        rightstage
        linear 2.5 off_right

    $ setWait(77.412,80.164)
    $ speak(JEFFERY, "Thanks yeah we go pretty deep with it.")



    hide jecka sc2

    show nicole sc2:
        leftcenterstage

    $ setWait(80.164,83.001)
    $ speak(NICOLE, "How did fucking with you backfire that hard?")
    show jeffery sc2:
        leftstage
    $ setWait(83.001,84.127)
    $ speak(JEFFERY, "What do you mean?")

    show nicole sc2:
        xzoom -1
        leftcenterstage

    $ setWait(84.127,89.674)
    $ speak(NICOLE, "Oh nothing sorry, that was a delayed response to an ex, the PTSD just brought it out of me.")
    $ setWait(89.674,93.886)
    $ speak(JEFFERY, "Cool. So where you headed for class, Nicole?")
    stop ambient fadeout 2

    menu:
        "GYM CLASS":
            jump scene_0026
        "PHOTOGRAPHY":
            jump scene_0027
label scene_0026:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0026.mp3")
    scene gym 1
    play ambient "audio/Ambience/gym_ambience.mp3" fadein 1.5

    show coach:
        rightstage

    show nicole sc2:
        leftstage

    show jeffery sc2:
        xzoom -1
        rightcenterstage

    show kylar sc2:
        xzoom -1
        leftcenterstage



    $ setWait(0.506,12.268)
    $ speak(COACH, "Look it's the first day.. no funny guys! No comedians! No bringers of the ha ha, okay? This year's gym class isn't last year's gym class. We're gonna really buckle down on physical fitness.")
    $ setWait(12.268,15.563)
    $ speak(NICOLE, "I'm fit as fuck I ain't buckling shit.")
    $ setWait(15.563,17.523)
    $ speak(COACH, "Young lady, what's your name?")

    show kylar sc2:
        xzoom -1
        leftcenterstage
        linear 1.3 leftstage

    show nicole sc2:
        leftstage
        linear 1 leftcenterstage

    $ setWait(17.523,20.234)
    $ speak(NICOLE, "Nicole, you want my phone number too?")
    $ setWait(20.234,24.947)
    $ speak(COACH, "This is only the first class, Nicole. You won't be a problem all year will ya?")
    $ setWait(24.947,26.24)
    $ speak(NICOLE, "No, sorry.")
    $ setWait(26.24,33.539)
    $ speak(COACH, "Good! Now everybody better dress out every class, if you don't it's a zero. Hit the locker rooms, I'll see ya back here in 10.")

    stop ambient fadeout 2

    menu:
        "GO TO LOCKER ROOM\nAND CHANGE":
            jump scene_0028
        "GYM SUCKS, I'M SITTING OUT":
            jump scene_0029
label scene_0027:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0027.mp3")
    scene photo classroom
    play ambient "audio/Ambience/Classroom_Ambience.mp3" fadein 2

    show girl_5 color2:
        xzoom -1
        xalign 0.56

    show girl_2 color2 unhappy:
        xzoom -1
        leftcenterstage

    show mr_white:
        rightstage



    $ setWait(0.46,9.552)
    $ speak(MR_WHITE, "So to not make the intro to Beginner's Photography too long, I'll simplify it by saying I'll have your shots looking superior by the end of this year!")

    show nicole sc2:
        off_left
        linear 1.5 leftstage

    $ setWait(9.552,13.264)
    $ speak(NICOLE, "Dude why did I pick an art class all these kids are annoyingly quirky.")
    show mr_white:
        rightstage
        linear 2 xalign 0.8

    $ setWait(13.264,15.933)
    $ speak(MR_WHITE, "So nice of you to join us, young lady.")
    $ setWait(15.933,19.187)
    $ speak(NICOLE, "You sound way too happy to be actually happy.")
    $ setWait(19.187,28.196)
    $ speak(MR_WHITE, "Quite observant. To make up for your tardiness perhaps you could help me out in the dark room? I need the chemicals cleansed for tomorrow's class.")

    stop ambient fadeout 2.5

    menu:
        "SKIP CAUSE HE ASKED YOU\nTO DO MANUAL LABOR":
            jump scene_0065
        "ROLL YOUR EYES\nWHILE AGREEING":
            jump scene_0075
label scene_0028:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0028.mp3")
    scene locker room
    play ambient "audio/ambience/Bathroom_Lockerroom_ambience.mp3" fadein 1.2

    show nicole changing angry:
        leftstage

    $ setWait(0.918,6.757)
    $ speak(NICOLE, "Where the hell did I put the shirt? Why does it even need the school logo? I'll just bring my own shitty shirts.")

    show coach smile:
        off_right
        linear 1.5 rightstage

    $ setWait(6.757,8.259)
    $ speak(COACH, "Having trouble, Nicole?")

    show nicole changing surprised:
        leftstage
        linear 0.3 xalign -0.12

    $ setWait(8.259,10.803)
    $ speak(NICOLE, "Um! Can you-- You can't be in here.")

    show coach smile:
        rightstage
        linear 2.5 rightcenterstage

    $ setWait(10.803,14.765)
    $ speak(COACH, "Saw you were lagging behind, thought you might need a spare shirt.")
    show nicole changing:
        xalign -0.12
    $ setWait(14.765,19.02)
    $ speak(NICOLE, "Oh thanks... Stop looking.. now, please.")
    $ setWait(19.02,23.9)
    $ speak(COACH, "Y'know something, you're feisty. I like that in my female students.")
    show nicole changing angry:
        xalign -0.12
    $ setWait(23.9,26.903)
    $ speak(NICOLE, "I got a feeling you like something else in your female students too.")
    $ setWait(26.903,31.49)
    $ speak(COACH, "See? You just snap back like that. I like it, it's sexy.")
    $ setWait(31.49,35.369)
    $ speak(NICOLE, "You are saying this to a 16 year old in the girls' locker room.")

    show coach:
        rightcenterstage
        linear 3.5 leftcenterstage

    $ setWait(35.369,39.999)
    $ speak(COACH, "C'mon, what's age? Look at you, you're mature enough.")
    menu:
        "SCREAM AS LOUD AS YOU CAN":
            jump scene_0030
        "HUMOR A LITERAL PEDOPHILE":
            jump scene_0032
label scene_0029:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0029.mp3")
    scene gym 2
    play ambient "audio/ambience/gym_ambience.mp3" fadein 1.5

    show nicole sc2:
        xzoom -1
        rightstage


    show jeffery sc2:
        rightcenterstage


    $ setWait(1.746,7.919)
    $ speak(JEFFERY, "...So gym class, showing our education system is pure evil.")
    $ setWait(7.919,9.921)
    $ speak(NICOLE, "Why do you talk like a cartoon?")

    show jeffery sc2:
        xzoom -1
        rightcenterstage

    $ setWait(9.921,13.466)
    $ speak(JEFFERY, "What do you mean? If I talked like a cartoon I'd go \"what's up, Doc?\"")
    $ setWait(13.466,19.889)
    $ speak(NICOLE, "No it's just this general \"ha ha I'm random\" cartoon channel talk. Have you ever watched television for adults?")
    $ setWait(19.889,22.392)
    $ speak(JEFFERY, "Wha.. Do you mean like porn?")
    $ setWait(22.392,24.728)
    $ speak(NICOLE, "No! Just normal-- nevermind.")
    show jeffery sc2 happy:
        rightcenterstage
    $ setWait(24.728,30.567)
    $ speak(JEFFERY, "Heh, cause I like some wild porn here and there. You probably couldn't handle it.")
    menu:
        "TIME FOR A VICIOUS\nREALITY CHECK":
            jump scene_0045
        "SEE IF HE'LL\nACTUALLY TELL YOU":
            jump scene_0047
label scene_0030:
    $ setVoiceTrack("audio/Scenes/0030.mp3")
    scene locker room

    show nicole changing scream:
        xalign -0.12

    show coach worried:
        leftcenterstage

    $ setWait(0.004,3.419)
    $ speak(NICOLE, "Aaahhh!! The gym teacher's trying to fuck!!")

    show coach worried:
        leftcenterstage
        linear 1 rightcenterstage

    $ setWait(3.419,5.504)
    $ speak(COACH, "Honey quiet down there, I need this job!")

    show nicole changing scream:
        xzoom -1
        leftstage

    $ setWait(5.504,8.382)
    $ speak(NICOLE, "He won't get his hands off this minor ass!!")

    show girl_1 gym:
        xzoom -1
        off_left
        linear 0.3 leftcenterstage

    show nicole changing:
        pause 0.3
        xzoom 1

    $ setWait(8.382,13.303)
    $ speak(GIRL_1, "Oh my god what're you doing the girls locker room!? Were you really grabbing some minor ass?")
    $ setWait(13.303,17.307)
    $ speak(NICOLE, "Minor as in \"underage\", I think my ass is pretty major to be honest.")

    show coach:
        rightcenterstage
        linear 1.5 xalign 0.59

    $ setWait(17.307,20.853)
    $ speak(COACH, "I've been at this school for 15 years, no one'll believe you!")
    $ setWait(20.853,22.438)
    $ speak(GIRL_1, "The security cameras will.")

    show coach furious:
        xalign 0.59
        pause 2
        linear 0.1 rightcenterstage
    $ setWait(22.438,26.775)
    $ speak(COACH, "I knew installing those spy ca-- security cameras would screw me over!")

    stop ambient fadeout 1.5
    jump scene_0031
label scene_0031:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0031.mp3")
    scene mall int
    play ambient "audio/ambience/mall_ambience.mp3" fadein 2

    show jecka designer:
        xzoom -1
        off_left
        linear 1.5 xalign .18

    $ setWait(2.375,6.879)
    $ speak(JECKA, "This might sound fucked up, but I'm almost happy our gym teacher was a pedophile.")

    show nicole designer:
        off_left
        linear 1.65 centerstage

    $ setWait(6.879,11.426)
    $ speak(NICOLE, "I'm definitely happy our gym teacher was a pedophile, do you see all this cool shit we bought?")
    $ setWait(11.426,13.928)
    $ speak(JECKA, "Yeah the settlement money's pretty nice.")

    show nicole designer:
        xzoom -1
        centerstage

    $ setWait(13.928,18.641)
    $ speak(NICOLE, "My Mom was like \"oh it's hush money\" I'm like whatever, the media wouldn't pay us nearly this much.")

    show jecka designer:
        xzoom -1
        xalign .18
        linear 3 off_right

    show nicole designer:
        xzoom 1
        centerstage
        linear 3 xalign 1.6

    stop ambient fadeout 4.5

    show black:
        alpha 0.0
        pause 1.9
        linear 2.4 alpha 1.0

    $ setWait(18.641,24.518)
    $ speak(JECKA, "Who needs morals when you have designer?")
    jump scene_0128
label scene_0032:
    $ setVoiceTrack("audio/Scenes/0032.mp3")
    scene locker room

    show nicole changing:
        xalign -0.12

    show coach smile:
        leftcenterstage

    $ setWait(0.093,3.796)
    $ speak(NICOLE, "I guess yeah. So what's up?")
    $ setWait(3.796,6.758)
    $ speak(COACH, "Just wanted a chat with a pretty girl...")
    $ setWait(6.758,7.759)
    $ speak(NICOLE, "About?")
    $ setWait(7.759,11.721)
    $ speak(COACH, "Oh I don't know uh... I just like lookin' at ya.")
    $ setWait(11.721,15.517)
    $ speak(NICOLE, "Why do girls say they like older men? You're just as boring as younger men.")
    $ setWait(15.517,19.062)
    $ speak(COACH, "I could show you a fun time a lot of these high school boys couldn't.")
    $ setWait(19.062,19.896)
    $ speak(NICOLE, "Oh yeah?")
    $ setWait(19.896,25.527)
    $ speak(COACH, "Yeah, and I'll prove it too. Hang out by the back entrance and I'll pick you up after school.")
    menu:
        "DATE YOUR GYM TEACHER":
            jump scene_0033
        "GET SEXUALLY HARASSED BY\nSOMEONE YOUR OWN AGE":
            jump scene_0037
label scene_0033:
    $ setVoiceTrack("audio/Scenes/0033.mp3")
    scene locker room

    show nicole changing:
        xalign -0.12
        linear 1.5 xalign -0.08

    show coach smile:
        leftcenterstage

    $ setWait(0.149,3.794)
    $ speak(NICOLE, "You have money to spend on me, right? Like at least a couple hundred?")
    $ setWait(3.794,7.423)
    $ speak(COACH, "Oh I got more than a couple hundred... like $370.")
    show nicole changing surprised:
        xalign -0.08
    $ setWait(7.423,10.718)
    $ speak(NICOLE, "Shit I'm just a kid, that's a lot for me, let's do it.")

    show nicole changing:
        xalign -.08

    show coach smile:
        xzoom -1
        leftcenterstage
        linear 1.9 rightcenterstage
        xzoom 1

    $ setWait(10.718,14.388)
    $ speak(COACH, "Sounds like a date, sexy. Can I call you sexy?")
    $ setWait(14.388,18.851)
    $ speak(NICOLE, "I mean the news would call me a victim but what do they know, right? Anyway I'll see ya tonight, man.")
    $ setWait(18.851,23.189)
    $ speak(COACH, "Nicole, Nicole, could you call me... coach?")
    stop ambient fadeout 3.4
    show black onlayer screens:
        alpha 0.0
        linear 2 alpha 1.0
        1
        linear 1 alpha 0.0
    show nicole changing flirt:
        xalign -.08
    $ setWait(23.189,25.855)
    $ speak(NICOLE, "See ya tonight, coach.")



    jump scene_0034
label scene_0034:
    $ setVoiceTrack("audio/Scenes/0034.mp3")

    play ambient "audio/Ambience/exterior_ambience.mp3" fadein 1
    scene onlayer master
    show black
    show barcade ext with Pause(2.831):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.831 zoom .6 truecenter

    scene barcade int

    play ambient "audio/ambience/barcade_ambience.mp3"

    show nicole sc2:
        leftcenterstage

    show coach:
        rightcenterstage


    $ setWait(2.831,6.209)
    $ speak(COACH, "So how's your drink so far?")
    $ setWait(6.209,12.883)
    $ speak(NICOLE, "My non-alcoholic Sprite is just wonderful... This date kinda sucks so far, could you get me high or something?")
    $ setWait(12.883,14.885)
    $ speak(COACH, "You want a sip of my Screwdriver?")

    show nicole sc2:
        leftcenterstage
        linear 0.2 xalign 0.4
        pause 0.1
        linear 0.3 leftcenterstage

    $ setWait(14.885,18.013)
    $ speak(NICOLE, "Sure thanks.... Can I have some more?")
    $ setWait(18.013,20.057)
    $ speak(COACH, "Some more? Sure, how many?")
    $ setWait(20.057,22.059)
    $ speak(NICOLE, "How many sips would equal 4 glasses?")
    $ setWait(22.059,27.064)
    $ speak(COACH, "Now I can't have you stumbling out of here wasted. People would start suspecting something.")
    $ setWait(27.064,29.483)
    $ speak(NICOLE, "I'm one third your age, that ship's sailed, coach.")
    show coach smile:
        rightcenterstage
    $ setWait(29.483,33.528)
    $ speak(COACH, "I know, it's such a rush. Are you feeling it too?")

    show nicole sc2:
        xzoom -1
        pause 2.9
        xzoom 1

    $ setWait(33.528,37.491)
    $ speak(NICOLE, "Um... Sure... So can I have money?")

    show nicole sc2:
        leftcenterstage

    $ setWait(37.491,43.58)
    $ speak(COACH, "Not so fast, sexy. I was thinking you could come back to my place to collect?")
    menu:
        "GO BACK TO HIS PLACE ALONE":
            jump scene_0035
        "MAKE A SCENE":
            jump scene_0036
label scene_0035:
    $ setVoiceTrack("audio/Scenes/0035.mp3")


    scene barcade int

    show nicole sc2 sly:
        leftcenterstage

    show coach smile:
        rightcenterstage

    $ setWait(0.092,1.585)
    $ speak(NICOLE, "Yeah Coach, I'm down.")
    $ setWait(1.585,5.339)
    $ speak(COACH, "Good girl. Just so you know, you're gonna have to earn it.")
    $ setWait(5.339,7.841)
    $ speak(NICOLE, "Do whatever you want, the money outweighs the trauma.")

    show coach smile:
        rightcenterstage
        pause 2.2
        linear 3 off_left

    $ setWait(7.841,11.053)
    $ speak(COACH, "C'mon, sexy. Let's get out of here.")

    show nicole sc2 sly:
        leftcenterstage
        pause 1.1
        xzoom -1
        linear 3 off_left

    $ setWait(11.053,13.555)
    $ speak(NICOLE, "After you, Coach.")

    stop ambient fadeout 1

    jump end_0039

label scene_0036:
    $ setVoiceTrack("audio/Scenes/0036.mp3")
    scene barcade int

    show nicole sc2 flirt:
        leftcenterstage

    show coach smile:
        rightcenterstage

    $ setWait(0.101,1.456)
    $ speak(NICOLE, "Fuck yeah I'll go home with you.")
    $ setWait(1.456,4.5)
    $ speak(COACH, "You just earned an A for the year, young lady.")
    $ setWait(4.5,7.503)
    $ speak(NICOLE, "Hey why don't you put your hand on my thigh? Gimme a preview.")
    $ setWait(7.503,10.131)
    $ speak(COACH, "I bet the skin on 'ems smooth and tight.")

    show coach:
        rightcenterstage
        linear 1.5 xalign 0.59

    show nicole sc2 sly:
        leftcenterstage

    $ setWait(10.131,12.341)
    $ speak(NICOLE, "Everything's tight when you're 16.")
    $ setWait(12.341,18.097)
    $ speak(COACH, "Oh that's nice. Of all the students I've dated, you're my favorite.")

    show nicole sc2 scream:
        leftcenterstage
        linear 0.3 leftstage
    $ setWait(18.097,20.308)
    $ speak(NICOLE, "Ah! Get your hand off my leg! Help! Stop!")

    show coach furious:
        xalign 0.59
        linear 0.7 leftcenterstage

    show nicole sc2 sly:
        leftstage

    $ setWait(20.308,21.517)
    $ speak(COACH, "What the fuck are you doing!?")

    show cop:
        off_right
        linear 1.2 leftcenterstage

    show coach worried:
        leftcenterstage
        pause 0.9
        linear 0.35 rightcenterstage


    $ setWait(21.517,24.771)
    $ speak(COP, "Sir, back away from the girl. What's the problem here?")

    show nicole sc2:
        leftstage
        linear 0.2 xalign 0.07

    $ setWait(24.771,29.525)
    $ speak(NICOLE, "This is my Gym teacher, he just started getting all sexual out of nowhere!")

    show nicole sc2:
        xalign 0.07
        linear 0.3 leftstage

    show cop:
        leftcenterstage
        xzoom -1

    $ setWait(29.525,30.777)
    $ speak(COP, "Is this true, sir?")

    show coach worried:
        rightcenterstage
        linear 0.2 xalign 0.72
        pause 0.2
        linear 0.1 rightcenterstage

    $ setWait(30.777,36.407)
    $ speak(COACH, "No-- Well yes but, they have the Gym teachers do sexual education now.")
    $ setWait(36.407,40.244)
    $ speak(NICOLE, "What's eating ass have to do with sexual education?")

    show cop:
        leftcenterstage
        xzoom 1
        pause 1.1
        xzoom -1

    $ setWait(40.244,43.414)
    $ speak(COP, "Is that true? Did you tell her to eat your ass out?")

    show coach worried:
        rightcenterstage
        pause 1.7
        linear 0.3 rightstage

    $ setWait(43.414,46.375)
    $ speak(COACH, "No, I wanted to eat hers-- I mean.. uh..")

    show cop:
        leftcenterstage
        xzoom -1
        pause 1
        xzoom 1

    show nicole sc2 smile:
        leftstage

    $ setWait(46.375,49.128)
    $ speak(NICOLE, "Sorry officer, that was just a false alarm.")


    $ setWait(49.128,50.088)
    $ speak(COACH, "Ugh thank god.")
    $ setWait(50.088,53.508)
    $ speak(NICOLE, "He just said he wanted to cum all over me, no big deal, right coach?")

    show coach furious:
        rightstage
        linear 0.15 rightcenterstage

    $ setWait(53.508,54.092)
    $ speak(COACH, "What!")

    show cop:
        leftcenterstage
        xzoom -1
        pause 3.8
        linear 0.2 xalign 0.56

    show coach worried:
        pause 4.1
        xzoom -1

    $ setWait(54.092,58.721)
    $ speak(COP, "Well Coach, the only place you're coming is downtown.")

    show coach furious:
        rightcenterstage
        xzoom -1
        linear 4.9 off_left

    show cop:
        xalign 0.56
        linear 5.5 off_farleft



    show nicole sc2 sly:
        leftstage
        pause 1.7
        linear 1.5 rightcenterstage
        xzoom -1


    $ setWait(58.721,63.226)
    $ speak(COACH, "You fucking bitch I'll kill you and your whole family too!")
    $ setWait(63.226,66.854)
    $ speak(NICOLE, "Hey man I got you arrested, you don't gotta do me that favor.")

    stop ambient fadeout 2
    jump scene_0056
label scene_0037:
    $ setVoiceTrack("audio/Scenes/0037.mp3")
    scene locker room

    show nicole changing:
        xalign -0.12

    show coach smile:
        leftcenterstage

    $ setWait(0.072,3.795)
    $ speak(NICOLE, "Hey man I'd love to catch an R but I got homework, it's a weeknight, y'know?")

    show coach smile:
        leftcenterstage
        linear 1.6 rightcenterstage

    $ setWait(3.795,10.135)
    $ speak(COACH, "Aw I guess you're right. Hey but one day we'll make something happen? I can't let my sexiest student get away now.")

    show nicole changing sly:
        xalign -0.12
        linear 1 leftstage

    $ setWait(10.135,12.137)
    $ speak(NICOLE, "Oh my god, you're so bad.")

    $ setWait(12.137,14.848)
    $ speak(COACH, "Your gym coach has been around the block, sweetie.")

    show nicole changing sly:
        leftstage
        pause 2.3
        xzoom -1
        linear 3.6 off_left

    $ setWait(14.848,21.604)
    $ speak(NICOLE, "Yeah well, sorry it didn't work out. I've had less periods than states in America, but again, sorry it didn't work out.")

    stop ambient fadeout 2

    jump scene_0038
label scene_0038:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0038.mp3")
    play ambient "audio/ambience/gym_ambience.mp3" fadein 1
    scene gym 3

    show nicole gym:
        leftcenterstage
    $ setWait(0.501,4.171)
    $ speak(NICOLE, "If your BMI is under 25 you should just automatically get an A.")

    show kylar gym:
        xzoom -1
        off_left
        linear 0.5 off_right
    $ setWait(4.171,5.38)
    $ speak(KYLAR, "Do something, bitch!")
    $ setWait(5.38,6.965)
    $ speak(NICOLE, "Dude shut up, who cares?")

    show kylar gym:
        xzoom 1
        off_right
        linear 0.6 rightstage
    $ setWait(6.965,10.469)
    $ speak(KYLAR, "Think you're getting far with that mentality? You gotta nut up, Nicole.")
    $ setWait(10.469,14.139)
    $ speak(NICOLE, "Oh sorry I didn't know dodgeball was a long term goal for you.")

    show kylar gym angry:
        rightstage
        pause 1.5
        linear 1 rightcenterstage

    $ setWait(14.139,17.559)
    $ speak(KYLAR, "Y'know, what if? What if it's a long term goal for me, huh?")
    $ setWait(17.559,22.564)
    $ speak(NICOLE, "I'd feel sorry for you cause I'm pretty sure they canceled Extreme Dodgeball like 2 years ago.")
    show kylar gym:
        rightcenterstage
    $ setWait(22.564,27.444)
    $ speak(KYLAR, "You saw that show too? That's sick! Y'know you're kinda cool for a girl.")
    $ setWait(27.444,33.659)
    $ speak(NICOLE, "Thanks.. uh.. sorry you're just not a person who warrants return compliments.")
    $ setWait(33.659,39.915)
    $ speak(KYLAR, "Man you're honest too.. that's kinda hot. Hey do you wanna, wanna like, hang out later?")
    menu:
        "SURE,\nLET'S SEE WHAT HE'S ABOUT":
            jump scene_0048
        "THIS DIPSHIT HAS NO CHANCE WITH ME":
            jump scene_0040

label end_0039:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0039" not in persistent.endings:
        $ persistent.endings.append("end_0039")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0039end with Pause (48.7):
        alpha 1.0
    return

label scene_0040:
    $ setVoiceTrack("audio/Scenes/0040.mp3")
    scene gym 3

    show nicole gym:
        leftcenterstage

    show kylar gym unhappy:
        rightcenterstage
    $ setWait(0.329,3.54)
    $ speak(NICOLE, "Are you seriously asking me out while taking dodgeball seriously?")
    $ setWait(3.54,10.089)
    $ speak(KYLAR, "No! I mean, well kinda. It could just be sex we don't need like a whole relationship.")
    $ setWait(10.089,16.804)
    $ speak(NICOLE, "Sorry I don't know the politically correct way of asking this, but.. are you actually retarded?")

    show kylar gym unhappy:
        xzoom -1
        rightcenterstage
        pause 1.1
        xzoom 1
    $ setWait(16.804,24.061)
    $ speak(KYLAR, "..Uh.. I don't know who told you, but when I got tested that was supposed to be a secret, fuckin' Trody can't keep his mouth shut!")
    $ setWait(24.061,27.231)
    $ speak(NICOLE, "Just having a friend named \"Trody\".")
    $ setWait(27.231,28.649)
    $ speak(KYLAR, "What're you trying to say?")
    $ setWait(28.649,32.403)
    $ speak(NICOLE, "You are a quintessential dipshit.")

    show kylar gym angry:
        rightcenterstage
        pause 2.5
        linear 0.4 xalign 0.57
    $ setWait(32.403,37.199)
    $ speak(KYLAR, "Quin.. uh.. I don't know what the fuck that means but I'm gonna kick your ass.")

    show nicole gym:
        leftcenterstage
        linear 0.6 leftstage

    $ setWait(37.199,39.493)
    $ speak(NICOLE, "You're gonna hit a girl? What the fuck is wrong with you?")

    show kylar gym angry:
        xalign 0.57
        pause 1.9
        linear 0.4 leftcenterstage
    $ setWait(39.493,44.164)
    $ speak(KYLAR, "Think I care? You don't know me, I'd beat the shit out my Mom if she was asking for it!")
    menu:
        "LET HIM SIMMER DOWN":
            jump scene_0041
        "GET THE NERD IN ON IT":
            jump scene_0042
label scene_0041:
    $ setVoiceTrack("audio/Scenes/0041.mp3")
    scene gym 3

    show nicole gym:
        leftstage

    show kylar gym angry:
        leftcenterstage
    $ setWait(0.253,3.173)
    $ speak(NICOLE, "Okay whatever, you're the only party who cares in this anyway.")

    show ball:
        off_left
        pause 2.3
        linear 0.3 off_right

    show kylar gym angry:
        xzoom -1
        leftcenterstage
        linear 2.3 rightstage
        pause 2
        linear 0.2 off_right


    $ setWait(3.173,9.596)
    $ speak(KYLAR, "Yeah don't test me again or there's gonna be trouble. Now I got balls to dodge.")

    show nicole gym sad:
        leftstage
        linear 1 leftcenterstage

    $ setWait(9.596,12.349)
    $ speak(NICOLE, "Why does everyone in the closet wanna kill me?")

    stop ambient fadeout 2
    jump scene_0057
label scene_0042:
    $ setVoiceTrack("audio/Scenes/0042.mp3")
    scene gym 3

    show nicole gym:
        leftstage

    show kylar gym angry:
        leftcenterstage


    show jeffery sc2 happy:
        off_right
        linear 1.5 rightstage
    $ setWait(0.253,2.046)
    $ speak(JEFFERY, "Hey, what'cha guys talking about?")
    show nicole gym sad:
        leftstage
    $ setWait(2.046,6.009)
    $ speak(NICOLE, "This guy here said he's gonna kick my ass, can you believe it?")

    show jeffery sc2:
        rightstage
        linear 0.6 rightcenterstage
    $ setWait(6.009,9.596)
    $ speak(JEFFERY, "Why would he hurt someone as beautiful as you?")
    $ setWait(9.596,10.972)
    $ speak(NICOLE, "I know, that's what I'm sayin'.")
    show jeffery sc2 angry:
        rightcenterstage

    show nicole gym:
        leftstage
    $ setWait(10.972,15.31)
    $ speak(JEFFERY, "You meat head jocks are all the same, treating women like objects!")

    show kylar gym:
        leftcenterstage
        xzoom -1

    $ setWait(15.31,18.897)
    $ speak(KYLAR, "So what, you treat girls like the plague- You never fuckin' touched one.")
    $ setWait(18.897,23.401)
    $ speak(JEFFERY, "Oh yeah, you're real tough. I'll have you know I'm saving myself for marriage!")
    $ setWait(23.401,29.49)
    $ speak(KYLAR, "You can't even tie your shoes, it's not \"saving\" when every store's closed you fuckin' bitchmo.")
    $ setWait(29.49,39.375)
    $ speak(JEFFERY, "Yeah well I'm pretty sure the only reason you harass girls is to make up for the time I saw you kissing the football captain!")

    show kylar gym angry:
        leftcenterstage
        linear 1 xalign 0.46

    show jeffery sc2:
        rightcenterstage
    $ setWait(39.375,41.628)
    $ speak(KYLAR, "...What the fuck did you just say?")
    $ setWait(41.628,45.298)
    $ speak(NICOLE, "Fucking your way to the top! Cool, dude.")

    show kylar gym angry:
        xalign 0.46
        xzoom 1
        linear 1 xalign 0.27

    $ setWait(45.298,48.509)
    $ speak(KYLAR, "I'm gonna break your whore nose right now you fucking bitch!")
    menu:
        "SCREAM FOR\nTHE GYM TEACHER":
            jump scene_0043
        "USE THE NERD\nAS A HUMAN SHIELD":
            jump scene_0044
label scene_0043:
    $ setVoiceTrack("audio/Scenes/0043.mp3")
    scene gym 3

    show nicole gym scream:
        leftstage

    show kylar gym angry:
        xalign 0.27

    show jeffery sc2:
        rightcenterstage

    $ setWait(0.178,2.43)
    $ speak(NICOLE, "Ah! He's gonna break my nose! Stop it!")

    show nicole gym:
        leftstage

    show jeffery sc2:
        xzoom -1
        rightcenterstage
        linear 1.1 off_right

    $ setWait(2.43,4.099)
    $ speak(KYLAR, "Screaming won't save you now.")

    show coach:
        off_right
        linear 2.5 rightcenterstage

    $ setWait(4.099,6.893)
    $ speak(COACH, "Hold on, hold on, what do you think you're doing?")

    show kylar gym unhappy:
        xzoom -1
        xalign 0.27
        linear 0.5 leftcenterstage

    $ setWait(6.893,11.189)
    $ speak(KYLAR, "Nothing coach, I'm just gonna punch this slut in the face until one of her eyes stop working.")
    show nicole gym:
        leftstage
    $ setWait(11.189,12.357)
    $ speak(NICOLE, "Jesus Christ--")
    show coach smile:
        rightcenterstage
    $ setWait(12.357,17.362)
    $ speak(COACH, "Kylar you won't be laying a hand on our lovely and very beautiful new student Nicole.")

    show kylar gym furious:
        xzoom -1
        leftcenterstage
        pause 4.2
        linear 0.05 xalign 0.35
        linear 0.05 xalign 0.31
        linear 0.05 xalign 0.35
        linear 0.05 xalign 0.31
        linear 0.05 xalign 0.35
        linear 0.05 xalign 0.31
        linear 0.05 xalign 0.35
        linear 0.05 xalign 0.31
        linear 0.02 leftcenterstage

    $ setWait(17.362,22.826)
    $ speak(KYLAR, "Ah! What the fuck, everyone's against me! I wanna go home and stab my hamster!")
    show coach:
        rightcenterstage
    $ setWait(22.826,27.914)
    $ speak(COACH, "That's it, son. I like that competitive fervor! Get out there and use it in regionals this Friday!")

    show kylar gym:
        xzoom -1
        leftcenterstage
        pause 1.7
        xzoom 1
        linear 0.7 off_left

    $ setWait(27.914,31.543)
    $ speak(KYLAR, "Heh, you got it coach!")
    $ setWait(31.543,35.005)
    $ speak(NICOLE, "So.. just no punishment?")

    show jeffery sc2 happy:
        xzoom 1
        off_right
        linear 1.5 rightstage

    $ setWait(35.005,38.633)
    $ speak(JEFFERY, "At least he got that monster off our back. Thanks, Mister Colby!")

    show coach smile:
        xzoom -1
        rightcenterstage

    $ setWait(38.633,45.807)
    $ speak(COACH, "No problem at all, Jeffery. I couldn't let him hurt the prettiest girl in class, I gotta look down someone's shirt for morning push-ups.")
    $ setWait(45.807,46.6)
    $ speak(NICOLE, "Are you kidding me?")

    show coach:
        xzoom -1
        rightcenterstage
        linear 1.8 off_right

    show jeffery sc2 happy:
        rightstage
        linear 1.4 leftcenterstage

    $ setWait(46.6,49.102)
    $ speak(JEFFERY, "True that, Sir.")
    $ setWait(49.102,51.479)
    $ speak(NICOLE, "Does he just say that in front of every girl?")
    $ setWait(51.479,54.107)
    $ speak(JEFFERY, "Only ones he thinks are really pretty!")

    show nicole gym:
        xzoom -1
        leftstage
        linear 1.5 off_left

    $ setWait(54.107,55.567)
    $ speak(NICOLE, "Ugh..")

    stop ambient fadeout 2

    jump scene_0057
label scene_0044:
    $ setVoiceTrack("audio/Scenes/0044.mp3")
    scene gym 3

    show nicole gym sad:
        leftstage

    show kylar gym angry:
        xalign 0.27

    show jeffery sc2:
        rightcenterstage

    $ setWait(0.125,2.67)
    $ speak(NICOLE, "Oh my god, please save me, Jeffery!")
    show jeffery sc2 angry:
        rightcenterstage
    $ setWait(2.67,6.465)
    $ speak(JEFFERY, "Okay buddy you wanna hurt the girl you gotta go through me.")

    show nicole gym:
        leftstage

    show kylar gym angry:
        xalign 0.27
        xzoom -1
        linear 0.5 leftcenterstage

    $ setWait(6.465,10.553)
    $ speak(KYLAR, "I was just gonna make her nose bleed, but I'll make sure you never walk again.")

    show kylar gym angry:
        leftcenterstage
        pause 1.5
        linear 0.2 off_right

    show jeffery sc2:
        rightcenterstage
        pause 1.58
        linear 0.11 off_right

    $ setWait(10.553,12.596)
    $ speak(JEFFERY, "Huh? You can't do that")
    $ setWait(12.596,13.931)
    $ speak(KYLAR, "I'm gonna fucking kill you!")

    show black:
        alpha 0.0
        linear 2.6 alpha 1.0

    $ setWait(13.931,20.226)
    $ speak(JEFFERY, "Oh god no! Ow! My glasses!")

    stop ambient fadeout 2
    jump scene_0058
label scene_0045:
    $ setVoiceTrack("audio/Scenes/0045.mp3")
    scene gym 2

    show nicole sc2:
        xzoom -1
        rightstage

    show jeffery sc2:
        xzoom -1
        rightcenterstage

    $ setWait(0.169,4.549)
    $ speak(NICOLE, "No one cares, just stop! For a nerd you're not too smart socially, huh?")
    show jeffery sc2 angry:
        xzoom -1
        rightcenterstage
    $ setWait(4.549,10.013)
    $ speak(JEFFERY, "Hey I'm just trying to have fun here. And I'm not a nerd, I'm a geek! There's a difference!")
    $ setWait(10.013,14.434)
    $ speak(NICOLE, "Sorry, which one grows up to be a rapist and which one grows up to be a pedophile?")
    $ setWait(14.434,20.064)
    $ speak(JEFFERY, "Ugh you and everyone else at this school.. I'm sick of being the butt of everyone's jokes!")
    $ setWait(20.064,21.024)
    $ speak(NICOLE, "Dude whatever.")
    $ setWait(21.024,25.82)
    $ speak(JEFFERY, "The blatant disrespect, snickering behind my back, fake love notes, beating me up--")
    $ setWait(25.82,28.197)
    $ speak(NICOLE, "Okay really didn't need your life story here.")
    $ setWait(28.197,33.995)
    $ speak(JEFFERY, "Stealing my stuff, egging my house, blackmailing me, calling my Mom at work and telling her I'm dead--")
    $ setWait(33.995,35.371)
    $ speak(NICOLE, "They go that hard here?")
    $ setWait(35.371,44.922)
    $ speak(JEFFERY, "And hanging me from the bleachers with rope weak enough to snap right before I choke to death.. I'm sick of all of it! And I guess you wanna be on that list too, huh?")
    menu:
        "LET HIS USUAL\nBULLY TAKE OVER":
            jump scene_0046
        "DELAY A\nPROBABLY INEVITABLE\nSCHOOL SHOOTING":
            jump scene_0059
label scene_0046:
    $ setVoiceTrack("audio/Scenes/0046.mp3")

    scene gym 2

    show nicole sc2:
        xzoom -1
        rightstage

    show jeffery sc2 angry:
        xzoom -1
        rightcenterstage

    show kylar gym:
        xzoom -1
        off_left
        linear 1.2 leftstage

    $ setWait(0.133,4.045)
    $ speak(KYLAR, "Hey what are you cripples doing? Finding new things to cut yourselves with?")
    $ setWait(4.045,7.924)
    $ speak(NICOLE, "Uh well actually this weirdo was just hitting on me, can you believe it?")
    $ setWait(7.924,9.968)
    $ speak(KYLAR, "Wow Jeff, didn't know you liked girls.")

    show jeffery sc2 angry:
        xzoom 1
        rightcenterstage

    $ setWait(9.968,14.013)
    $ speak(JEFFERY, "Who is this Jeff you speak of? The name's Jeffery thank you.")
    $ setWait(14.013,16.933)
    $ speak(NICOLE, "Yeah see? More of that cartoon sounding shit.")
    $ setWait(16.933,18.643)
    $ speak(KYLAR, "He won't stop talking to you or something?")
    $ setWait(18.643,21.479)
    $ speak(NICOLE, "Yeah, make yourself useful and kick his ass for me?")

    $ setWait(21.479,23.398)
    $ speak(KYLAR, "You're hot enough to listen to, sure.")

    show jeffery sc2:
        rightcenterstage

    show kylar gym:
        xzoom -1
        leftstage
        linear 5 xalign .36

    show black:
        alpha 0.0
        linear 5.2 alpha 1.0

    stop ambient fadeout 6

    $ setWait(23.398,30.237)
    $ speak(JEFFERY, "Oh please no! Not in the face! My glasses are brand new! Can't we just read some manga instead?")
    jump scene_0058
label scene_0047:
    $ setVoiceTrack("audio/Scenes/0047.mp3")
    scene gym 2

    show nicole sc2 sly:
        xzoom -1
        rightstage

    show jeffery sc2:
        xzoom -1
        rightcenterstage

    $ setWait(0.337,1.63)
    $ speak(NICOLE, "Try me.")
    $ setWait(1.63,8.803)
    $ speak(JEFFERY, "Huh, most girls just scream and run when I say that. You're different.")
    $ setWait(8.803,11.014)
    $ speak(NICOLE, "Well are you gonna tell me or not?")
    $ setWait(11.014,12.432)
    $ speak(JEFFERY, "Why do you wanna know?")

    show nicole sc2 sly:
        xzoom -1
        rightstage
        pause 6
        linear 1 xalign .87

    $ setWait(12.432,21.149)
    $ speak(NICOLE, "Uh everybody knows the coolest guys have depraved fetishes, have you been on the internet? Maybe I'm looking for a boyfriend who can keep up with me.")

    show jeffery sc2 blush:
        xzoom 1
        rightcenterstage
        pause 1.7
        xzoom -1

    show nicole sc2:
        xzoom -1
        xalign .87

    $ setWait(21.149,27.489)
    $ speak(JEFFERY, "Uh.. uh.. alright. See me at lunch today, maybe we could talk about it then.")

    show jeffery sc2 blush:
        xzoom -1
        rightcenterstage

    $ setWait(27.489,28.698)
    $ speak(NICOLE, "I'm so there.")
    $ setWait(28.698,32.744)
    $ speak(JEFFERY, "Awesome, finally someone to share my escapism with.")
    $ setWait(32.744,33.828)
    $ speak(NICOLE, "Escapism?")
    $ setWait(33.828,44.714)
    $ speak(JEFFERY, "Yeah I get lost in all these weird websites to get away from my gun nut step dad. I think he was in Iraq or something. Doesn't matter anyway, I think Mom's already looking for a new guy.")

    show nicole sc2:
        xzoom 1
        xalign .82

    $ setWait(44.714,49.302)
    $ speak(NICOLE, "A house full of depraved porn and firearms, what could possibly go wrong?")
    $ setWait(49.302,50.053)
    $ speak(JEFFERY, "What was that?")

    show nicole sc2 sly:
        xzoom -1
        xalign .87

    $ setWait(50.053,54.574)
    $ speak(NICOLE, "Oh-- just, I've wanted a chat like this for so long.")

    stop ambient fadeout 1.8

    jump scene_0060
label scene_0048:
    $ setVoiceTrack("audio/Scenes/0048.mp3")
    scene gym 3

    show nicole gym:
        leftcenterstage

    show kylar gym unhappy:
        rightcenterstage

    $ setWait(0.629,2.756)
    $ speak(NICOLE, "Like hang out where?")
    $ setWait(2.756,6.801)
    $ speak(KYLAR, "Oh y'know my place maybe? I got this really cool stereo.")
    $ setWait(6.801,10.096)
    $ speak(NICOLE, "Your Dad bought a really cool stereo? That's cool.")

    show kylar gym unhappy:
        rightcenterstage
        xzoom -1
        pause 1.75
        xzoom 1

    $ setWait(10.096,13.975)
    $ speak(KYLAR, "So.. so are you down?")
    $ setWait(13.975,17.145)
    $ speak(NICOLE, "I guess sure, when do I come by?")
    $ setWait(17.145,22.651)
    $ speak(KYLAR, "Any time tonight, my parents are out of town trying to find a boarding school to put me in. Sound good?")
    $ setWait(22.651,23.86)
    $ speak(NICOLE, "Yeah I'll swing by.")
    show kylar gym:
        rightcenterstage
    $ setWait(23.86,26.863)
    $ speak(KYLAR, "Sweet you're down to fuck and everything, this is gonna rock.")
    $ setWait(26.863,30.45)
    $ speak(NICOLE, "Whoa no, the only thing down is my serotonin levels.")
    $ setWait(30.45,33.036)
    $ speak(KYLAR, "What's serotonin? Is that printer ink?")

    stop ambient fadeout 5

    show black:
        alpha 0.0
        linear 3.4 alpha 1.0

    $ setWait(33.036,36.848)
    $ speak(NICOLE, "Y-Yes I'll go now stop talking to me.")


    jump scene_0049
label scene_0049:
    play ambient "audio/Ambience/neighborhood_ambience_night.mp3" fadein 1
    $ setVoiceTrack("audio/Scenes/0049.mp3")

    scene onlayer master
    show black
    show house kylar night with Pause(3.331):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 3.3 zoom .6 truecenter

    scene home kylar
    play ambient "audio/Ambience/House_Night_Ambience.mp3"

    show nicole sc2:
        off_farleft
        linear 3 leftstage

    show kylar sc2:
        off_left
        xzoom -1
        linear 3.1 leftcenterstage
        xzoom 1



    $ setWait(3.337,13.805)
    $ speak(KYLAR, "But yeah so I'm pretty into cool shit, y'know not like cool cool shit, but kinda that step away from the regular cool shit like just doing my own thing y'know?")
    $ setWait(13.805,19.019)
    $ speak(NICOLE, "All I asked was \"are you paying for the pizza\" and you just went into that.")
    show kylar sc2 unhappy:
        leftcenterstage
    $ setWait(19.019,25.817)
    $ speak(KYLAR, "Whatever y'know stuff at school, just on my mind and everything. What do you wanna talk about? Lacrosse maybe?")
    menu:
        "SEE WHAT SHITTY\nMUSIC HE LIKES":
            jump scene_0050
        "TALK SHIT ABOUT OTHER KIDS":
            jump scene_0051
        "SEE IF THERE'S ANYTHING TO STEAL AROUND HERE":
            jump scene_0052
label scene_0050:
    $ setVoiceTrack("audio/Scenes/0050.mp3")
    scene home kylar
    show nicole sc2:
        leftstage

    show kylar sc2 unhappy:
        leftcenterstage

    $ setWait(0.578,6.751)
    $ speak(NICOLE, "Uh.. do you listen to music? Or is it just Eye Of The Tiger pregame playlists?")
    $ setWait(6.751,11.089)
    $ speak(KYLAR, "Yeah I like music, I like bands. Guitars and drums.")
    $ setWait(11.089,15.51)
    $ speak(NICOLE, "...Yep that about covers it. What bands specifically?")
    $ setWait(15.51,19.681)
    $ speak(KYLAR, "You know the... Midnight Supernova.")
    $ setWait(19.681,23.852)
    $ speak(NICOLE, "Who the fuck are the Midnight Supernova? When did they start?")
    $ setWait(23.852,27.188)
    $ speak(KYLAR, "Like.. just now cause I just made it up.")
    $ setWait(27.188,33.194)
    $ speak(NICOLE, "Someone who cares would awkwardly try to continue this conversation, but I don't...")
    jump scene_0053
label scene_0051:
    $ setVoiceTrack("audio/Scenes/0051.mp3")
    scene home kylar
    show nicole sc2:
        leftstage

    show kylar sc2 unhappy:
        leftcenterstage
    $ setWait(0.213,3.216)
    $ speak(NICOLE, "Does Lacrosse involve beating the shit out of that one kid?")
    $ setWait(3.216,4.592)
    $ speak(KYLAR, "What one kid?")
    $ setWait(4.592,7.971)
    $ speak(NICOLE, "The one who likes Japan a lot.. Jeffery?")
    show kylar sc2:
        leftcenterstage
    $ setWait(7.971,12.559)
    $ speak(KYLAR, "What? Oh yeah totally me and the guys fuck with his ass all the time.")
    $ setWait(12.559,13.852)
    $ speak(NICOLE, "Yeah? How many fingers?")
    show kylar sc2 unhappy:
        leftcenterstage
    $ setWait(13.852,17.856)
    $ speak(KYLAR, "Not like that! Just throwing lacrosse balls at him and watching him jump.")
    $ setWait(17.856,21.735)
    $ speak(NICOLE, "Nice, yeah him suffering just makes me feel good for some reason.")
    show kylar sc2:
        leftcenterstage
    $ setWait(21.735,27.115)
    $ speak(KYLAR, "Yeah that's hot, speaking of that, you know that one girl Jecka? I can't remember her last name.")
    show nicole sc2 smile:
        leftstage
    $ setWait(27.115,30.702)
    $ speak(NICOLE, "I know her, she dresses really expensive and everything? She's cool.")
    show kylar sc2 unhappy:
        leftcenterstage
    $ setWait(30.702,33.038)
    $ speak(KYLAR, "Yeah cool like in a stuck up bitch way.")
    show nicole sc2:
        leftstage
    $ setWait(33.038,34.247)
    $ speak(NICOLE, "What'd she do to you?")
    $ setWait(34.247,42.547)
    $ speak(KYLAR, "Nothing, but girls with that sort of attitude.. I don't know. Like I wanna have sex with her to knock her down a few pegs.")
    $ setWait(42.547,44.299)
    $ speak(NICOLE, "...What the fuck is wrong with you?")
    $ setWait(44.299,45.925)
    $ speak(KYLAR, "How is that wrong?")
    $ setWait(45.925,49.637)
    $ speak(NICOLE, "Whatever, all men are rapists anyway you're just a drop in the bucket.")
    jump scene_0053
label scene_0052:
    $ setVoiceTrack("audio/Scenes/0052.mp3")
    scene home kylar
    show nicole sc2:
        leftstage

    show kylar sc2 unhappy:
        leftcenterstage
    $ setWait(0.215,2.342)
    $ speak(NICOLE, "Is there even money in Lacrosse?")
    $ setWait(2.342,5.637)
    $ speak(KYLAR, "Well the pizza party after games is like $80 or something.")
    $ setWait(5.637,9.265)
    $ speak(NICOLE, "No like memorabilia. Autographs, anything?")
    $ setWait(9.265,13.102)
    $ speak(KYLAR, "Well my regional trophy's made of gold so pretty valuable.")
    $ setWait(13.102,16.439)
    $ speak(NICOLE, "I tapped it on the way in here, pretty sure it's plastic.")
    $ setWait(16.439,18.858)
    $ speak(KYLAR, "I guess the paint's made of real gold then.")
    $ setWait(18.858,23.071)
    $ speak(NICOLE, "Does anyone famous play lacrosse? Have a signed ball or something?")
    $ setWait(23.071,30.745)
    $ speak(KYLAR, "The greatest lacrosse player of this era is probably Cody Simpson, but I lost one of his signed jerseys last year. It was worth so much.")
    $ setWait(30.745,32.997)
    $ speak(NICOLE, "Oh wow for real? How much we talking?")

    show kylar sc2:
        leftcenterstage
        linear 0.3 xalign 0.4
        pause 0.5
        linear 0.3 xalign 0.48
        pause 0.8
        linear 0.1 leftcenterstage

    $ setWait(32.997,36.251)
    $ speak(KYLAR, "Dude.. bro like.. $90 dollars!")
    $ setWait(36.251,41.256)
    $ speak(NICOLE, "So there's no money in playing it, no money collecting it, what's the point?")
    $ setWait(41.256,50.306)
    $ speak(KYLAR, "That's kinda what makes lacrosse so awesome, it's not about the money or commercials. The true payment comes in honor! Girls so dig honor.")
    $ setWait(50.306,54.852)
    $ speak(NICOLE, "Honor won't pay for my new outfits, how do you buy into any of this shit? Who cares?")
    jump scene_0053
label scene_0053:
    $ setVoiceTrack("audio/Scenes/0053.mp3")
    scene home kylar
    show nicole sc2:
        leftstage

    show kylar sc2:
        leftcenterstage
    $ setWait(0.161,11.506)
    $ speak(KYLAR, "Wow it's like.. it's just the way you don't even give a fuck. It's hot, I like it. All these girls always freaking out over whatever but you... you wanna try like going steady?")
    $ setWait(11.506,15.51)
    $ speak(NICOLE, "Going steady? People still say that? Like a relationship?")
    $ setWait(15.51,17.887)
    $ speak(KYLAR, "Yeah you could be my girlfriend and everything.")
    $ setWait(17.887,18.972)
    $ speak(NICOLE, "What a treat.")
    $ setWait(18.972,21.099)
    $ speak(KYLAR, "So how 'bout it? You wanna date?")
    menu:
        "REJECT HIM COLDLY":
            jump scene_0054
        "PLAY AROUND\nWITH THIS LEVERAGE":
            jump scene_0055
label scene_0054:
    $ setVoiceTrack("audio/Scenes/0054.mp3")
    scene home kylar
    show nicole sc2:
        leftstage

    show kylar sc2:
        leftcenterstage
    $ setWait(0.338,3.132)
    $ speak(NICOLE, "Uh.. how does \"hell no\" sound?")
    show kylar sc2 unhappy:
        leftcenterstage
    $ setWait(3.132,3.841)
    $ speak(KYLAR, "..What?")
    $ setWait(3.841,7.345)
    $ speak(NICOLE, "The 20 minutes I've been here's already way more than I could chew.")
    $ setWait(7.345,10.348)
    $ speak(KYLAR, "You don't think athletes are emotional? We can be deep.")
    $ setWait(10.348,20.441)
    $ speak(NICOLE, "It's not that you're an athlete, you're a lacrosse player. There's no offhand chance I miss out on a millionaire husband. Literally no one gives a shit about lacrosse but the people who play it.")
    $ setWait(20.441,23.277)
    $ speak(KYLAR, "That's not true, my Dad likes lacrosse.")
    $ setWait(23.277,25.53)
    $ speak(NICOLE, "And did he play it?")
    $ setWait(25.53,28.032)
    $ speak(KYLAR, "Yeah but not right now.")
    $ setWait(28.032,32.828)
    $ speak(NICOLE, "..Are you pretending to be stupid? There's like no way, this is some big joke, right?")
    $ setWait(32.828,37.041)
    $ speak(KYLAR, "No I wouldn't pull a joke on you, I'm just stupid-- totally retarded.")
    $ setWait(37.041,42.129)
    $ speak(NICOLE, "You ever heard that one phrase? We can either choose intelligence or happiness?")
    $ setWait(42.129,44.382)
    $ speak(KYLAR, "Um.. no?")
    $ setWait(44.382,51.931)
    $ speak(NICOLE, "Well assuming it's real, I don't feel bad telling you to never talk to me again. Your dipshit brain shouldn't take it too hard.")

    show kylar sc2 sad:
        xzoom -1
        leftcenterstage

    $ setWait(51.931,55.476)
    $ speak(KYLAR, "N-no.. you don't understand..")
    $ setWait(55.476,58.688)
    $ speak(NICOLE, "You're not.. are you.. crying?")
    $ setWait(58.688,62.733)
    $ speak(KYLAR, "It's just.. no.. you're being mean to me..")
    $ setWait(62.733,65.695)
    $ speak(NICOLE, "Whoa hey um.. don't, y'know.")
    $ setWait(65.695,68.03)
    $ speak(KYLAR, "Maybe coach was right.")
    $ setWait(68.03,70.491)
    $ speak(NICOLE, "Um.. sorry?")

    show kylar sc2 sad:
        xzoom 1
        leftcenterstage

    $ setWait(70.491,77.748)
    $ speak(KYLAR, "No it's whatever. I'll just go to the Lacrosse convention alone this weekend.. that's why I wanted a girlfriend I guess.")
    $ setWait(77.748,79.667)
    $ speak(NICOLE, "Oh you're going alone?")
    $ setWait(79.667,82.753)
    $ speak(KYLAR, "I guess.. whatever..")
    $ setWait(82.753,83.921)
    $ speak(NICOLE, "This is awkward.")
    $ setWait(83.921,88.342)
    $ speak(KYLAR, "I'll just jump off the roof so I have a good excuse to not go..")
    $ setWait(88.342,92.096)
    $ speak(NICOLE, "Ugh.. Do you want me to go to the lacrosse convention with you?")
    show kylar sc2 unhappy:
        leftcenterstage
    $ setWait(92.096,95.057)
    $ speak(KYLAR, "Y-you would do that?")
    $ setWait(95.057,96.267)
    $ speak(NICOLE, "I guess.")
    show kylar sc2:
        leftcenterstage
    $ setWait(96.267,100.438)
    $ speak(KYLAR, "Aw cool, I'll pick you up this weekend. Thanks.")
    $ setWait(100.438,102.356)
    $ speak(NICOLE, "Can I get some Percocet for going?")
    $ setWait(102.356,106.986)
    $ speak(KYLAR, "Oh yeah, my prescriptions on the dresser. Just take it when you walk out.")

    show nicole sc2:
        leftstage
        xzoom -1
        linear 1.4 off_left

    show black:
        alpha 0.0
        pause 1.7
        linear 2.5 alpha 1.0

    stop ambient fadeout 6

    $ setWait(106.986,112.671)
    $ speak(NICOLE, "I guess I'm walking out now then.")



    jump scene_0129
label scene_0055:
    $ setVoiceTrack("audio/Scenes/0055.mp3")
    scene home kylar
    show nicole sc2 smile:
        leftstage

    show kylar sc2:
        leftcenterstage
    $ setWait(0.246,1.789)
    $ speak(NICOLE, "No.")
    show kylar sc2 sad:
        leftcenterstage
    $ setWait(1.789,6.21)
    $ speak(KYLAR, "No? Just like that? Give me a chance, dude.")
    show nicole sc2:
        leftstage
    $ setWait(6.21,10.422)
    $ speak(NICOLE, "Sorry but I'm... too smart to date you.")
    $ setWait(10.422,12.091)
    $ speak(KYLAR, "How am I not smart enough? How?")
    $ setWait(12.091,13.634)
    $ speak(NICOLE, "Do you see this room?")
    $ setWait(13.634,17.012)
    $ speak(KYLAR, "What cause I like sports? We're not all dumb jocks, y'know.")
    $ setWait(17.012,24.937)
    $ speak(NICOLE, "Who cares if you like sports? You're just boring. Like yeah your coach gives you free Percocet and everything but how does that make you cool?")
    show kylar sc2 unhappy:
        leftcenterstage
    $ setWait(24.937,27.439)
    $ speak(KYLAR, "So, what do I do?")
    $ setWait(27.439,29.567)
    $ speak(NICOLE, "Impress me or die trying.")
    $ setWait(29.567,31.861)
    $ speak(KYLAR, "So if I die you'll be my girlfriend?")
    $ setWait(31.861,44.915)
    $ speak(NICOLE, "No as in-- look, I'm sick of the same boring kid trying to take me out on his parent's money. I want a guy who's not afraid to ruin his life for me. And when I see that I'll know your worth dating.")
    $ setWait(44.915,47.751)
    $ speak(KYLAR, "Oh.. I don't know..")

    show nicole sc2 sly:
        leftstage
        pause 1.3
        xzoom -1
        linear 1.3 xalign -0.17

    $ setWait(47.751,49.879)
    $ speak(NICOLE, "Lost interest huh? Good, nice talking--")
    $ setWait(49.879,50.838)
    $ speak(KYLAR, "But I'll do it!")

    show nicole sc2:
        xalign -.17
        xzoom 1
        linear .75 leftstage

    $ setWait(50.838,51.463)
    $ speak(NICOLE, "What?")
    $ setWait(51.463,57.553)
    $ speak(KYLAR, "I don't have it all figured out yet but like, I'm gonna do some amazing shit to make you love me. You're so worth it for sure.")

    show nicole sc2 smile:
        leftstage

    $ setWait(57.553,60.681)
    $ speak(NICOLE, "Aww. If I didn't have PTSD I'd be blushing right now.")
    show kylar sc2:
        leftcenterstage
    $ setWait(60.681,64.935)
    $ speak(KYLAR, "Awesome! I'll see you at school next week, I got a few things to work on.")
    show nicole sc2:
        leftstage
    $ setWait(64.935,66.645)
    $ speak(NICOLE, "So I can go now?")
    $ setWait(66.645,69.315)
    $ speak(KYLAR, "Yeah... is there something wrong?")
    $ setWait(69.315,74.111)
    $ speak(NICOLE, "No, just surprised I didn't get sexually assaulted for telling you \"no\".")

    show keys:
        xalign 0.3
        yalign 1.5
        pause 3
        linear .3 yalign 0.72

    $ setWait(74.111,78.991)
    $ speak(KYLAR, "Aw nah I wouldn't do that. You want my key? Like to my house.")
    $ setWait(78.991,80.91)
    $ speak(NICOLE, "...Why would I want a key to your house?")

    show keys:
        yalign 0.72 xalign 0.3
        pause 2.2
        linear 0.1 xalign 0.31
        linear 0.1 xalign 0.29
        linear 0.1 xalign 0.29
        linear 0.1 xalign 0.31
        linear 0.08 xalign 0.3
        pause .68
        linear 0.07 xalign 0.24

    $ setWait(80.91,84.914)
    $ speak(KYLAR, "Just letting you know you're always welcome. Take my key, take it-- take my key.")

    show nicole sc2:
        xzoom -1
        leftstage
        linear 3 off_left

    show keys:
        xalign 0.16
        linear 3 xalign -0.17


    $ setWait(84.914,86.29)
    $ speak(NICOLE, "Okay.")

    stop ambient fadeout 2

    jump scene_0106
label scene_0056:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0056.mp3")
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 2
    scene cafeteria int

    show nicole sc3:
        leftcenterstage

    show jecka sc3 unhappy:
        rightcenterstage

    $ setWait(0.05,3)
    $ speak(JECKA, "")
    $ setWait(3,5.586)
    $ speak(JECKA, "...Well are you gonna tell me?")
    $ setWait(5.586,7.129)
    $ speak(NICOLE, "Tell you what?")
    $ setWait(7.129,11.592)
    $ speak(JECKA, "You know what. Everyone's texting about what happened at the barcade yesterday.")
    $ setWait(11.592,17.473)
    $ speak(NICOLE, "That's what they call those places? Men will invent any phrase to make their video games less embarrassing.")
    show jecka sc3 surprised:
        rightcenterstage
    $ setWait(17.473,21.602)
    $ speak(JECKA, "So it is true. What happened? Did Coach promise you a good grade or something?")
    $ setWait(21.602,25.648)
    $ speak(NICOLE, "First of all, how does anyone even know I was there? I didn't file any charges.")
    show jecka sc3 unhappy:
        rightcenterstage

    $ setWait(25.648,28.984)
    $ speak(JECKA, "Some guy who goes here snapped a picture of you at the table with him.")
    $ setWait(28.984,30.611)
    $ speak(NICOLE, "Wow a real vigilante.")

    show flash:
        alpha 0
        pause 6.3
        linear 0.02 alpha 1
        linear 0.2 alpha 0
    $ setWait(30.611,38.035)
    $ speak(JECKA, "No he just does that for his private collection of girls who go here. You getting caught with the gym teacher on camera was pure coincidence.")
    $ setWait(38.035,42.665)
    $ speak(NICOLE, "Okay well I kinda.. baited him into harassing me.")

    show jecka sc3 surprised:
        rightcenterstage
        linear .3 xalign .54

    $ setWait(42.665,48.128)
    $ speak(JECKA, "Nicole! That's fucked up, what if you get harassed for real one day and no one believes you cause of that?")
    $ setWait(48.128,53.801)
    $ speak(NICOLE, "Oh yeah, I guess a date with your high school gym teacher was a perfectly fine situation. I'll leave it alone next time, thanks.")
    $ setWait(53.801,58.681)

    show jecka sc3 unhappy:
        xalign .54
        linear .7 rightcenterstage

    $ speak(JECKA, "Okay point taken, bitch. So what, he groped you and someone saw or?")
    $ setWait(58.681,62.142)
    $ speak(NICOLE, "Well no, I told him to grope me and just screamed.")
    $ setWait(62.142,65.771)
    $ speak(JECKA, "Oh my god.. so that was premeditated on your part.")
    $ setWait(65.771,66.855)
    $ speak(NICOLE, "Mostly..")
    $ setWait(66.855,71.36)
    $ speak(JECKA, "So why'd you even go out with him in the first place if you knew it'd just end in a shit show?")
    $ setWait(71.36,80.786)
    $ speak(NICOLE, "Y'know, don't have a great answer for that. I just did it cause I could. The more I thought about it, the more leverage I knew I had.")
    $ setWait(80.786,84.206)
    $ speak(JECKA, "But he's twice your size he could've killed you.")
    $ setWait(84.206,96.051)
    $ speak(NICOLE, "Yeah but not when other people were around. The second he decided to date a minor he lost the game of life. Now he's in jail, lost his job, most of his friends.. if he had a family they probably bailed too.")
    $ setWait(96.051,99.43)
    $ speak(JECKA, "And if someone tries to put the blame on the minor they look..")

    show black:
        alpha 0.0
        pause 5
        linear 2.5 alpha 1.0

    stop ambient fadeout 9
    $ setWait(99.43,108.645)
    $ speak(NICOLE, "Like a monster, exactly. Susan B. Anthony or whoever the fuck got women this far, but I got it from here.")



    jump scene_0128
label scene_0057:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0057.mp3")
    scene cafeteria int 2
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1

    show nicole gym:
        off_left
        linear 2.5 leftcenterstage

    show jecka sc2 unhappy:
        rightcenterstage

    $ setWait(1.503,3.425)
    $ speak(JECKA, "What's that?")
    $ setWait(3.425,4.635)
    $ speak(NICOLE, "What's what?")
    $ setWait(4.635,6.22)
    $ speak(JECKA, "The gym clothes?")
    show nicole gym sad:
        leftcenterstage
    $ setWait(6.22,12.017)
    $ speak(NICOLE, "Oh yeah, the heat's cranked way too high here so I just left class in this. I can finally breathe, y'know?")
    $ setWait(12.017,16.689)
    $ speak(JECKA, "Okay well you're the first girl I've ever met who isn't cold 24/7.")

    show nicole gym:
        xzoom -1
        leftcenterstage

    $ setWait(16.689,19.358)
    $ speak(NICOLE, "Yep not cold at all.")
    $ setWait(19.358,20.442)
    $ speak(JECKA, "...What's wrong?")

    show nicole gym:
        xzoom 1
        leftcenterstage

    $ setWait(20.442,25.364)
    $ speak(NICOLE, "I skipped changing to get out of gym quick as possible. Trying to avoid that lacrosse kid following me.")
    $ setWait(25.364,27.199)
    $ speak(JECKA, "What's roid rage want with you?")
    $ setWait(27.199,33.622)
    $ speak(NICOLE, "He asked me out and I pretty clearly told him to screw off. It's like white guys who like running can't take \"no\" for an answer.")
    $ setWait(33.622,36.167)
    $ speak(JECKA, "I wish I had like 5%% of your confidence.")
    $ setWait(36.167,37.459)
    $ speak(NICOLE, "How is that confidence?")
    $ setWait(37.459,41.505)
    $ speak(JECKA, "Blatantly telling some scary dude to get lost? I could never do that.")

    show black:
        alpha 0.0
        pause 3.5
        linear 2.5 alpha 1.0

    stop ambient fadeout 8

    $ setWait(41.505,49.918)
    $ speak(NICOLE, "It's not that I'm confident, I'm just too lazy to give a shit.")

    jump scene_0128
label scene_0058:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0058.mp3")
    scene cafeteria int
    play ambient "audio/ambience/cafeteria_ambience.mp3" fadein 1.4

    show nicole sc2:
        off_left
        linear 2.6 leftcenterstage

    show jecka sc2:
        rightcenterstage

    $ setWait(0.109,2.503)
    $ speak(JECKA, "Hey how ya doing?")
    $ setWait(2.503,4.755)
    $ speak(NICOLE, "Uh.. just coping.")
    show jecka sc2 unhappy:
        rightcenterstage
    $ setWait(4.755,6.256)
    $ speak(JECKA, "...Coping with what?")
    $ setWait(6.256,8.926)
    $ speak(NICOLE, "Just the power I have as a girl.")
    $ setWait(8.926,11.136)
    $ speak(JECKA, "Did you come here from the feminist seminar?")
    $ setWait(11.136,12.554)
    $ speak(NICOLE, "No, gym.")
    $ setWait(12.554,13.889)
    $ speak(JECKA, "What happened?")
    $ setWait(13.889,19.103)
    $ speak(NICOLE, "Like.. okay, I pretty much just got the lacrosse kid to beat the shit out of the anime kid.")
    show jecka sc2:
        rightcenterstage
    $ setWait(19.103,21.396)
    $ speak(JECKA, "Jealous! I wanted to watch.")
    $ setWait(21.396,23.065)
    $ speak(NICOLE, "Wasn't much of a fight honestly.")
    show jecka sc2 unhappy:
        rightcenterstage
    $ setWait(23.065,28.237)
    $ speak(JECKA, "Oh, did he do the nerd fight thing where he just hugged onto him really tight? Yeah, fine with missing that.")
    $ setWait(28.237,36.787)
    $ speak(NICOLE, "Dude it's not even the fight, just like, how I got it to happen. I didn't promise a date, or sex, or anything and he just went with it.")
    $ setWait(36.787,40.082)
    $ speak(JECKA, "The way you're processing this is kinda scary to be honest.")
    $ setWait(40.082,42.292)
    $ speak(NICOLE, "What? You never manipulated someone before?")
    show jecka sc2 worried:
        rightcenterstage
    $ setWait(42.292,48.173)
    $ speak(JECKA, "No, I technically do it all the time I've just never verbalized it like that.. Are we bad people?")
    $ setWait(48.173,53.47)
    $ speak(NICOLE, "I don't know, I'm still just trying to process why he'd fist fight for someone he barely knows.")
    show jecka sc2 unhappy:
        rightcenterstage
    $ setWait(53.47,55.222)
    $ speak(JECKA, "Cause you're pretty.")
    $ setWait(55.222,56.306)
    $ speak(NICOLE, "...Pretty what?")
    $ setWait(56.306,58.725)
    $ speak(JECKA, "No, you're just really pretty.")
    $ setWait(58.725,60.686)
    $ speak(NICOLE, "But like that pretty? No way.")
    $ setWait(60.686,65.357)
    $ speak(JECKA, "If you're gonna be one of those girls who fish for compliments 24/7 I'm gonna find someone else to sit with.")
    $ setWait(65.357,68.61)
    $ speak(NICOLE, "No seriously, like what are they worked up over?")
    $ setWait(68.61,74.283)
    $ speak(JECKA, "You're cute, long flowing hair, and... big boobs.")
    $ setWait(74.283,75.826)
    $ speak(NICOLE, "Okay I was fishing for compliments.")
    $ setWait(75.826,76.535)
    $ speak(JECKA, "Knew it.")
    $ setWait(76.535,80.622)
    $ speak(NICOLE, "But seriously like.. why aren't we consciously using this to our advantage?")
    $ setWait(80.622,83.959)
    $ speak(JECKA, "Using being pretty? It's called stripping.")
    $ setWait(83.959,91.967)
    $ speak(NICOLE, "Stripping's for women who never had the conversation we're having right now. Dumb bitches who were like \"wow everyone's so helpful, you really think he's nice cause he's into me?\".")
    show jecka sc2:
        rightcenterstage
    $ setWait(91.967,94.72)
    $ speak(JECKA, "That's like half of my friends oh my god. \"What? No way\"")
    show nicole sc2 sly:
        leftcenterstage
    $ setWait(94.72,99.683)
    $ speak(NICOLE, "And then, and then \"Oh no I'm 26 and ran out of guys hitting me up, life is so unfair\"")
    $ setWait(99.683,102.352)
    $ speak(JECKA, "Well does anyone really run out of guys?")
    show nicole sc2:
        leftcenterstage
    $ setWait(102.352,104.146)
    $ speak(NICOLE, "You run out of good ones real quick.")
    $ setWait(104.146,111.737)
    $ speak(JECKA, "Oh yeah.. So this new philosophy, unveiled manipulation, how long are you running with it? 'Till graduation?")

    show nicole sc2 sly:
        leftcenterstage

    show black:
        alpha 0.0
        pause 2
        linear 2.5 alpha 1.0

    stop ambient fadeout 5

    $ setWait(111.737,117.864)
    $ speak(NICOLE, "'Till death.")

    jump scene_0128
label scene_0059:
    $ setVoiceTrack("audio/Scenes/0059.mp3")
    scene gym 2

    show nicole sc2:
        xzoom -1
        rightstage

    show jeffery sc2 angry:
        xzoom -1
        rightcenterstage

    $ setWait(0.177,3.046)
    $ speak(NICOLE, "Uh.. I guess not.")
    show jeffery sc2:
        rightcenterstage
    $ setWait(3.046,5.381)
    $ speak(JEFFERY, "You.. you don't?")
    $ setWait(5.381,9.469)
    $ speak(NICOLE, "Well the way you put it made it seem like way too much effort anyway so..")
    show jeffery sc2 happy:
        rightcenterstage
    $ setWait(9.469,12.555)
    $ speak(JEFFERY, "Wow y'know you're actually kinda nice.")
    show nicole sc2 surprised:
        rightstage
    $ setWait(12.555,13.556)
    $ speak(NICOLE, "That's nice?")
    show nicole sc2:
        rightstage
    $ setWait(13.556,19.354)
    $ speak(JEFFERY, "Yeah will you sit at lunch with me? I got a table all to myself right outside the pizza line.")
    $ setWait(19.354,23.733)
    $ speak(NICOLE, "I'd like to but I told someone else I was gonna sit with them today so sorry.")
    show jeffery sc2:
        rightcenterstage
    $ setWait(23.733,25.777)
    $ speak(JEFFERY, "Oh, who?")

    show nicole sc2:
        xzoom 1
        pause 2
        xzoom -1

    $ setWait(25.777,30.948)
    $ speak(NICOLE, "Fuck I forgot I'm new here.. are you gonna buy me lunch or anything or is this a full on charity seating?")
    $ setWait(30.948,36.704)
    $ speak(JEFFERY, "I pack lunch but my mom always makes too much, we can share mine. How does that sound?")
    $ setWait(36.704,41.959)
    $ speak(NICOLE, "Uh, your lunch isn't some weird shit, right? Like hot dogs slices in white rice?")
    $ setWait(41.959,46.756)
    $ speak(JEFFERY, "Nah, good old fashioned tuna fish sandwiches. A classic if you ask me.")
    $ setWait(46.756,50.176)
    $ speak(NICOLE, "And the easiest sandwich to fuck up...")
    $ setWait(50.176,52.679)
    $ speak(JEFFERY, "So are you going or..?")
    $ setWait(52.679,53.554)
    $ speak(NICOLE, "Fine.")
    show jeffery sc2 happy:
        rightcenterstage
    $ setWait(53.554,58.601)
    $ speak(JEFFERY, "Awesomeness! I can tell you all about the new cartoon episodes if you missed any last week.")
    $ setWait(58.601,63.564)
    $ speak(NICOLE, "Shucks, yeah y'know I've actually missed all the new cartoons for the last 200 weeks.")

    show jeffery sc2:
        xzoom 1
        rightcenterstage
        linear 7 off_farleft

    $ setWait(63.564,67.276)
    $ speak(JEFFERY, "Ugh, so behind. Why would you do this to yourself?")

    show nicole sc2:
        xzoom -1
        rightstage
        linear 6.3 off_left

    show black:
        alpha 0.0
        pause 2
        linear 2.5 alpha 1.0

    stop ambient fadeout 6.5

    $ setWait(67.276,73.78)
    $ speak(NICOLE, "Yeah I have no idea why I'm doing this to myself either.")



    jump scene_0129
label scene_0060:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0060.mp3")

    scene cafeteria int
    play ambient "audio/ambience/cafeteria_ambience.mp3" fadein 1.5

    show nicole sc2 sly:
        xalign .39

    show jeffery sc2 blush:
        xalign .61

    $ setWait(0.396,3.958)
    $ speak(NICOLE, "So you like 'em how much taller than you exactly?")
    $ setWait(3.958,11.423)
    $ speak(JEFFERY, "At least like 12 feet taller. Preferably 50. I wanna be picked up with only 2 of her fingers.")
    $ setWait(11.423,13.217)
    $ speak(NICOLE, "And what do you call that again?")
    $ setWait(13.217,21.767)
    $ speak(JEFFERY, "It's a giantess fetish, a woman so tall she can't even see those minute details about me, like how I can't tie my shoes.")
    $ setWait(21.767,25.354)
    $ speak(NICOLE, "Yeah I wouldn't want anyone to see that either. This is cool, what else?")
    $ setWait(25.354,31.11)
    $ speak(JEFFERY, "Really? Uh well, I like it when cute girls walk all over me.")
    $ setWait(31.11,34.488)
    $ speak(NICOLE, "Huh, y'know most people hate when they're taken advantage of.")
    $ setWait(34.488,41.704)
    $ speak(JEFFERY, "No, I mean.. literally walk all over me. Love to be stepped on by a cute pair of feet.")
    $ setWait(41.704,43.914)
    $ speak(NICOLE, "Well hey it beats stepping on a scale, right?")
    $ setWait(43.914,54.466)
    $ speak(JEFFERY, "But yeah, unfortunately most of my fetishes can only be realized through my anime. The realm of the living isn't quite ready for 50 foot tall vixens.")
    $ setWait(54.466,57.386)
    $ speak(NICOLE, "Yeah the real world sucks hard, dude.")
    $ setWait(57.386,61.39)
    $ speak(JEFFERY, "Did I mention how I liked girls with cat ears and tails?")
    $ setWait(61.39,63.559)
    $ speak(NICOLE, "Do they meow when you have sex with them?")
    $ setWait(63.559,66.103)
    $ speak(JEFFERY, "Well I.. wouldn't know.")
    $ setWait(66.103,67.688)
    $ speak(NICOLE, "Haven't done one yet?")
    $ setWait(67.688,71.191)
    $ speak(JEFFERY, "I haven't done.. anyone before.")

    stop ambient fadeout 2

    show black:
        alpha 0.0
        linear 2.5 alpha 1.0

    $ setWait(71.191,75.093)
    $ speak(NICOLE, "Shocker.")


    jump scene_0061
label scene_0061:

    $ setVoiceTrack("audio/Scenes/0061.mp3")

    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 2
    scene onlayer master
    show black

    show school front with Pause(2.917):
        zoom 1.0 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.917 zoom 1.1 truecenter

    scene school int 2

    play ambient "audio/ambience/hallway_ambience.mp3"

    show jeffery sc3:
        xzoom -1
        off_left
        linear 3 leftcenterstage

    $ setWait(2.917,6.004)
    $ speak(JEFFERY, "I wonder if the library has volume 31 yet..")

    show jecka sc3:
        off_right
        linear 2 rightcenterstage

    $ setWait(6.004,9.716)
    $ speak(JECKA, "Hey there Jeffery! Things better with your Dad yet?")

    show jeffery sc3:
        xzoom -1
        leftcenterstage

    $ setWait(9.716,16.681)
    $ speak(JEFFERY, "Oh hello, Jecka. Unfortunately no. He used my toothbrush to clean out his new assault rifle he bought from China.")
    $ setWait(16.681,20.935)
    $ speak(JECKA, "Wow messed up, much? Anyway could you buy me another Diet Coke?")
    $ setWait(20.935,25.773)
    $ speak(JEFFERY, "Sorry but I can't anymore, my mom's been wondering where all my lunch money's been going.")
    show jecka sc3 worried:
        rightcenterstage
    $ setWait(25.773,28.735)
    $ speak(JECKA, "Awww you're mean, you don't like me anymore.")
    $ setWait(28.735,30.945)
    $ speak(JEFFERY, "Again I'm sorry I just don't know--")
    show jecka sc3 mean:
        rightcenterstage
    $ setWait(30.945,34.824)
    $ speak(JECKA, "Maybe I should grow 40 feet, then you'd really like me!")
    show jeffery sc3 emb:
        leftcenterstage
    $ setWait(34.824,37.91)
    $ speak(JEFFERY, "Hey! How'd you? ..Rrrgh!")

    show guy_2 smirk:
        xzoom -1
        off_left
        linear 1.1 xalign 0.03

    $ setWait(37.91,41.247)
    $ speak(GUY_2, "Maybe if you took your shoes off and stepped on his face!")

    show kylar sc2:
        xzoom -1
        off_left
        linear 1.3 xalign -0.15

    show girl_2 color2:
        off_right
        linear 1 xalign 1.1

    show jeffery sc3 emb:
        xzoom 1
        leftcenterstage


    $ setWait(41.247,43.75)
    $ speak(JEFFERY, "I can't believe this! She told everyone?")

    show jeffery sc3 emb:
        leftcenterstage
        xzoom 1
        pause 0.7
        xzoom -1

    $ setWait(43.75,48.713)
    $ speak(JECKA, "It's okay, Jeffery! Run away with me, I'll stuff you in my back pocket.")

    show jeffery sc3 emb:
        leftcenterstage

    $ setWait(48.713,50.381)
    $ speak(JEFFERY, "Ugh just shut up!")

    show girl_2 color2:
        xalign 1.1
        linear 0.6 xalign 0.85

    $ setWait(50.381,52.467)
    $ speak(GIRL_2, "He's feisty today, me-ow!")

    show jecka sc3:
        xzoom -1
        rightcenterstage

    $ setWait(52.467,54.594)
    $ speak(JECKA, "Oh my god I almost forgot about that.")



    $ setWait(54.594,56.179)
    $ speak(GIRL_2, "You have any cat nip for us?")

    show jecka sc3:
        rightcenterstage
        xzoom 1

    $ setWait(56.179,58.639)
    $ speak(JECKA, "Yeah pet us, make us purr!")

    show jeffery sc3 emb:
        xzoom -1
        leftcenterstage
        linear 0.8 off_right

    show guy_2 smirk:
        xzoom -1
        xalign .03
        pause 0.6
        linear 0.5 leftcenterstage

    show kylar sc2:
        xzoom -1
        pause 0.7
        linear 0.5 leftstage

    show jecka sc3 mean:
        rightcenterstage
        pause 0.5
        xzoom -1

    show girl_2 color2:
        pause 0.7
        xzoom -1
        linear 0.4 xalign .9

    show black onlayer screens:
        alpha 0.0
        linear 5 alpha 1.0
        4
        linear 1.5 alpha 0.0

    stop ambient fadeout 6


    $ setWait(58.639,67.565)
    $ speak(JEFFERY, "I can't believe this!")

    hide jeffery
    hide kylar sc2
    hide guy_2
    hide girl_2 color2
    hide jecka sc3

    scene classroom int 3

    play ambient "audio/Ambience/Classroom_Ambience.mp3" fadein 1.4

    show lynn:
        xzoom -1
        leftstage

    show jeffery black:
        centerstage

    show girl_2 unhappy:
        xalign .77

    show guy_2 color2:
        xalign 1.07

    show black onlayer screens:
        alpha 1.0
        0.8
        linear 3.2 alpha 0.0

    $ setWait(67.565,79.035)
    $ speak(LYNN, "So again, while I find the notes flattering, the boys need to quit writing \"bad bitch\" on my office door. I'll start tracking who left them if it continues.")
    show guy_2 color2 smirk:
        xalign 1.07

    hide black onlayer screens
    $ setWait(79.035,80.912)
    $ speak(GUY_2, "Well it definitely wasn't Jeffery.")

    show lynn:
        xzoom -1
        leftstage
        linear 0.5 xalign 0.1

    $ setWait(80.912,81.537)
    $ speak(LYNN, "Oh?")
    show guy_2 color2:
        xalign 1.07
    $ setWait(81.537,82.789)
    $ speak(GUY_2, "Fuck, you heard that?")
    $ setWait(82.789,85.249)
    $ speak(LYNN, "Why is it definitely not Jeffery?")
    show girl_2:
        xalign .77

    show guy_2 color2 smirk:
        xalign 1.07
    $ setWait(85.249,88.086)
    $ speak(GIRL_2, "Cause you're not a cat!")
    show girl_2 unhappy:
        xalign .77

    show guy_2 color2:
        xalign 1.07
    $ setWait(88.086,94.592)
    $ speak(LYNN, "Settle down now, I've heard the rumors going around about him and you should all be ashamed of yourselves!")
    $ setWait(94.592,97.011)
    $ speak(JEFFERY, "Thank you, I was really--")
    $ setWait(97.011,103.267)
    $ speak(LYNN, "Just because he prefers alternative forms of sexual intercourse does not mean he should be ridiculed.")
    show jeffery black emb:
        centerstage
    $ setWait(103.267,104.477)
    $ speak(JEFFERY, "Ugh..")
    show girl_2:
        xalign .77
    $ setWait(104.477,109.357)
    $ speak(GIRL_2, "Sorry I'm a little out of the loop.. what do you mean by alternative?")
    $ setWait(109.357,110.108)
    $ speak(JEFFERY, "Oh god.")
    $ setWait(110.108,118.616)
    $ speak(LYNN, "Jeffery here prefers to be stepped on by women who look like cats as opposed to standard intercourse with a human woman.")
    $ setWait(118.616,120.743)
    $ speak(JEFFERY, "Will this stop?")

    show lynn:
        xzoom 1
        xalign 0.08
        linear 3 off_farleft

    show jeffery black:
        centerstage

    show girl_2:
        xalign .77
        pause 0.7
        linear 5 off_farleft

    show guy_2 color2:
        xalign 1.07
        pause 0.8
        linear 5.1 off_farleft

    show girl_3:
        off_right
        linear 5.7 off_left


    show nicole sc3:
        xzoom -1
        off_farright
        linear 6 leftstage



    $ setWait(120.743,126.04)
    $ speak(LYNN, "Class dismissed!")
    $ setWait(126.04,128.084)
    $ speak(JEFFERY, "You did this.")

    hide jecka sc2
    hide guy_2 color2
    hide lynn
    hide girl_2

    show nicole sc3:
        xzoom 1
        leftstage

    $ setWait(128.084,129.585)
    $ speak(NICOLE, "Did what?")
    $ setWait(129.585,135.675)
    $ speak(JEFFERY, "Told everyone my darkest secrets... that was in confidence.")
    $ setWait(135.675,137.593)
    $ speak(NICOLE, "Guess I did, sorry.")
    $ setWait(137.593,146.269)
    $ speak(JEFFERY, "You ruined my life.. I haven't touched my manga in forever. Not even cartoons entertain me anymore.")
    $ setWait(146.269,147.854)
    $ speak(NICOLE, "Relatable.")
    $ setWait(147.854,153.818)
    $ speak(JEFFERY, "Do you even care? Do the results of your actions mean anything to you?")
    $ setWait(153.818,156.779)
    $ speak(NICOLE, "Yeah, when they affect me, sure.")
    $ setWait(156.779,163.494)
    $ speak(JEFFERY, "...No one in the realm of the living ever liked me anyway. Maybe things would make sense if I was dead.")
    $ setWait(163.494,165.58)
    $ speak(NICOLE, "Maybe.")
    $ setWait(165.58,173.846)
    $ speak(JEFFERY, "I've had to start taking medication since you betrayed me. I also waited for everyone to leave just so you'd be the only one to hear this.")
    $ setWait(173.846,181.846)
    $ speak(JEFFERY, "Tonight when Mom's out with her new boyfriend, I'm gonna take the entire bottle. I'm going to kill myself.")
    show nicole sc3 surprised:
        leftstage
    $ setWait(181.846,183.097)
    $ speak(NICOLE, "What?")
    $ setWait(183.097,189.353)
    $ speak(JEFFERY, "You chose to start this... but I won't give you a choice in stopping it.")
    menu:
        "CALL HIS BLUFF":
            jump scene_0062
        "GIRL HORMONES MAKE ME FEEL GUILTY":
            jump scene_0064
label scene_0062:
    $ setVoiceTrack("audio/Scenes/0062.mp3")
    scene classroom int 3
    show nicole sc3:
        leftstage

    show jeffery black:
        centerstage
    $ setWait(0.201,5.041)
    $ speak(NICOLE, "I'm sorry, did you think I have any form of emotional attachment to you?")
    $ setWait(5.041,11.84)
    $ speak(JEFFERY, "Why else would you have talked to me in the first place? Why would you have lunch with someone you don't like?")
    $ setWait(11.84,17.011)
    $ speak(NICOLE, "It... It was funny? I knew you'd say some embarrassing shit?")
    $ setWait(17.011,23.852)
    $ speak(JEFFERY, "So you used me... You were a new student trying to look cool, so you just used me.")
    $ setWait(23.852,31.734)
    $ speak(NICOLE, "No shit. In what world does a girl like me take interest in you? If you're that fucking stupid maybe you should kill yourself.")
    $ setWait(31.734,45.248)
    $ speak(JEFFERY, "Fine... I'll give you your satisfaction, but not before getting mine first... You're the only girl I ever loved, even if it wasn't real.")

    show nicole sc3:
        leftstage
        pause 2.2
        xzoom -1
        linear 3 off_left

    $ setWait(45.248,50.336)
    $ speak(NICOLE, "You knew me for 2 days, bye.")

    stop ambient fadeout 2

    jump end_0063

label end_0063:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0063" not in persistent.endings:
        $ persistent.endings.append("end_0063")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0063end with Pause (38.8):
        alpha 1.0
    return
label scene_0064:
    $ setVoiceTrack("audio/Scenes/0064.mp3")
    scene classroom int 3
    show nicole sc3:
        leftstage

    show jeffery black:
        centerstage
    $ setWait(0.453,4.835)
    $ speak(NICOLE, "I mean.. you don't have to kill yourself over this, do you?")
    $ setWait(4.835,12.718)
    $ speak(JEFFERY, "In the realm of the living I am nothing more than a punchline for others' amusement. This is not the purpose I desired.")
    $ setWait(12.718,15.054)
    $ speak(NICOLE, "Well what is?")
    $ setWait(15.054,16.764)
    $ speak(JEFFERY, "..I don't know.")
    $ setWait(16.764,19.517)
    $ speak(NICOLE, "So if you die now you'll never know.")
    $ setWait(19.517,24.146)
    $ speak(JEFFERY, "Don't try to talk me out of it, there's really no place for people like me.")
    $ setWait(24.146,26.607)
    $ speak(NICOLE, "What're \"people like you\" like?")
    $ setWait(26.607,30.694)
    $ speak(JEFFERY, "I want 40 foot tall women with cat features to step on me.")

    show nicole sc3:
        leftstage
        linear 2 xalign 0.20

    $ setWait(30.694,33.906)
    $ speak(NICOLE, "You really think that's the end of the world though?")
    $ setWait(33.906,35.157)
    $ speak(JEFFERY, "What do you mean?")
    $ setWait(35.157,38.16)
    $ speak(NICOLE, "So you want more than missionary, big deal.")
    $ setWait(38.16,43.207)
    $ speak(JEFFERY, "Okay so it's not the end of the world, it's still the end of my social life.")
    $ setWait(43.207,53.05)
    $ speak(NICOLE, "Jeffery.. What social life? All you did was read anime books before, you're still reading anime books now. Did you stop jerking off to porn of comically tall women?")
    $ setWait(53.05,53.801)
    $ speak(JEFFERY, "No.")
    $ setWait(53.801,58.514)
    $ speak(NICOLE, "So what's the problem? Seems like everything's going according to plan.")
    $ setWait(58.514,67.148)
    $ speak(JEFFERY, "You know.. you're right. The only thing that's different is everyone knows now. Who cares?")
    $ setWait(67.148,69.525)
    $ speak(NICOLE, "Yeah, before they just assumed it.")
    $ setWait(69.525,73.279)
    $ speak(JEFFERY, "Gosh thanks, Nicole. You're a really good friend.")
    show nicole sc3 surprised:
        xalign 0.2
    $ setWait(73.279,75.156)
    $ speak(NICOLE, "Uh-- I'm sorry, what was that last word?")

    show nicole sc3:
        xalign 0.2

    show jeffery black:
        centerstage
        pause 5.15
        linear 2.5 off_left

    $ setWait(75.156,83.372)
    $ speak(JEFFERY, "Maybe I'll see ya in lunch tomorrow. Company always keeps the suicidal thoughts away, see ya!")

    hide jeffery black

    show black:
        alpha 0.0
        pause 2.2
        linear 2.5 alpha 1.0

    stop ambient fadeout 6.5

    $ setWait(83.372,89.791)
    $ speak(NICOLE, "This is what empathy gets you?")
    jump scene_0129
label scene_0065:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        1.8
        linear 2 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0065.mp3")
    play ambient "audio/ambience/Bathroom_Lockerroom_ambience.mp3" fadein 2.5
    scene bathroom

    show crispin sc2:
        xzoom -1
        leftstage

    show nicole sc2:
        xzoom -1
        off_right
        linear 2.5 rightstage


    $ setWait(0.001,2.627)
    $ speak(NICOLE, "")
    $ setWait(2.627,5.338)
    $ speak(CRISPIN, "Oh hey I know you, what's up?")
    $ setWait(5.338,7.34)
    $ speak(NICOLE, "This is the girls' bathroom.")
    $ setWait(7.34,10.677)
    $ speak(CRISPIN, "Really? Nah. No way? So what brings you here?")
    $ setWait(10.677,14.431)
    $ speak(NICOLE, "Hmm, what would bring a girl to the girl's bathroom?")
    $ setWait(14.431,15.765)
    $ speak(CRISPIN, "Skipping?")

    show nicole sc2:
        xzoom -1
        rightstage
        linear 2 leftcenterstage

    show crispin sc2:
        xzoom -1
        leftstage
        pause 1
        linear 1.5 rightcenterstage
        xzoom 1

    $ setWait(15.765,17.017)
    $ speak(NICOLE, "Duh, now get out.")

    $ setWait(17.017,19.31)
    $ speak(CRISPIN, "Aw come on wait, what class you cutting?")

    show nicole sc2:
        xalign 0.265
        xzoom 1

    show crispin sc2:
        xzoom 1
        rightcenterstage

    $ setWait(19.31,23.481)
    $ speak(NICOLE, "Photography. The teacher tried making me do shit for free and I am not about that.")
    show crispin sc2:
        rightcenterstage
    $ setWait(23.481,26.526)
    $ speak(CRISPIN, "Photography? Oh me too! Crazy!")
    $ setWait(26.526,30.155)
    $ speak(NICOLE, "So even if I don't skip I can't avoid you.. great.")
    $ setWait(30.155,32.907)
    $ speak(CRISPIN, "You're a cool girl, y'know that?")
    $ setWait(32.907,34.159)
    $ speak(NICOLE, "...What?")
    $ setWait(34.159,35.91)
    $ speak(CRISPIN, "I just like you, y'know?")
    $ setWait(35.91,39.372)
    $ speak(NICOLE, "Dude get in line, nobody knows how to leave me the fuck alone here.")
    $ setWait(39.372,52.677)
    $ speak(CRISPIN, "So honest, like.. I feel like I could really open up to you. You have a lot of.. emotional conversations? I listen to a lot of deep bands so I can never find a girl that can keep up with me in that department.")
    $ setWait(52.677,57.223)
    $ speak(NICOLE, "Did.. You just threw that \"deep bands\" thing in there with no context.")
    $ setWait(57.223,60.393)
    $ speak(CRISPIN, "Come on.. can I at least know your name?")
    $ setWait(60.393,61.436)
    $ speak(NICOLE, "Nicole...")
    $ setWait(61.436,66.066)
    $ speak(CRISPIN, "Oh, Hi Nicole, you wanna have a sitdown with me? Y'know, talk it up?")
    menu:
        "NICELY SAY YOU\nAREN'T INTERESTED":
            jump scene_0066
        "LET'S SEE HOW\nNOT DEEP HE IS":
            jump scene_0067
label scene_0066:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0066.mp3")
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1.5
    scene cafeteria int 2

    show jecka sc2:
        rightcenterstage

    show nicole sc2:
        off_left
        linear 2.5 leftcenterstage

    $ setWait(1.556,3.207)
    $ speak(JECKA, "Hey, stranger.")
    $ setWait(3.207,4.751)
    $ speak(NICOLE, "Hi yeah.")
    show jecka sc2 unhappy:
        rightcenterstage
    $ setWait(4.751,6.753)
    $ speak(JECKA, "You seem drained, what's going on?")
    $ setWait(6.753,9.589)
    $ speak(NICOLE, "I just came here from skipping photography.")
    $ setWait(9.589,11.716)
    $ speak(JECKA, "And it didn't go well because?")
    $ setWait(11.716,14.927)
    $ speak(NICOLE, "Some fucking psycho was waiting for me in the girls' bathroom.")
    $ setWait(14.927,17.138)
    $ speak(JECKA, "I thought they fired that mailman.")
    $ setWait(17.138,23.728)
    $ speak(NICOLE, "Uh.. evidently a different psycho. He was eager tell me about his taste in music.")
    $ setWait(23.728,27.774)
    $ speak(JECKA, "Oh, sounds like Crispin. Or any of the other Guitar 1 students.")
    $ setWait(27.774,33.654)
    $ speak(NICOLE, "Yeah I think his name was that, wasn't really paying attention between the awkward icebreakers and 30 minutes of crying.")
    $ setWait(33.654,34.947)
    $ speak(JECKA, "Why was he crying?")
    $ setWait(34.947,45.208)
    $ speak(NICOLE, "He wanted to \"open up\" to me in a public restroom for like no reason, he doesn't know me. I told him \"no\" and he just wouldn't stop crying about how he loves me and no one understands him, whatever.")
    $ setWait(45.208,48.461)
    $ speak(JECKA, "God, being a girl... it's a gift and a curse.")
    $ setWait(48.461,52.089)
    $ speak(NICOLE, "It's like I was socially trapped, hopefully one \"no\" keeps him at bay.")
    $ setWait(52.089,57.553)
    $ speak(JECKA, "With those types it never does. If they know how to reach you it kinda just doesn't stop.")
    $ setWait(57.553,59.889)
    $ speak(NICOLE, "You know from experience?")
    $ setWait(59.889,66.646)
    $ speak(JECKA, "Yeah! Not him specifically but just guys acting all vulnerable so I pay attention to them. Sick of it, but what can you do?")
    $ setWait(66.646,69.482)
    $ speak(NICOLE, "Commit egregious acts of disrespect.")
    $ setWait(69.482,71.484)
    $ speak(JECKA, "Is that what you did?")
    $ setWait(71.484,76.405)
    $ speak(NICOLE, "Uh.. now that I think about it I was way too nice in that whole exchange.")
    $ setWait(76.405,80.743)
    $ speak(JECKA, "How nice? Did you apologize at any point? Did you say \"sorry\"?")
    $ setWait(80.743,84.455)
    $ speak(NICOLE, "I was.. pretty cold and detached I thought.")

    show jecka sc2 unhappy:
        rightcenterstage
        linear 2.5 xalign .56

    $ setWait(84.455,87.583)
    $ speak(JECKA, "Did. You. Say. Sorry?")

    show nicole sc2 scream:
        leftcenterstage

    $ setWait(87.583,88.501)
    $ speak(NICOLE, "Fuck, I did.")

    show jecka sc2 unhappy:
        xalign .56
        linear 0.4 rightcenterstage

    $ setWait(88.501,89.627)
    $ speak(JECKA, "You dumb slut!")

    show nicole sc2:
        leftcenterstage

    $ setWait(89.627,92.463)
    $ speak(NICOLE, "I didn't even do anything to him, why the fuck would I apologize?")
    $ setWait(92.463,97.218)
    $ speak(JECKA, "It's those girl hormones, we're genetically programmed to put up with bullshit.")
    $ setWait(97.218,99.387)
    $ speak(NICOLE, "How much longer until graduation?")
    $ setWait(99.387,102.139)
    $ speak(JECKA, "20 months. Can you last?")

    show black:
        alpha 0.0
        2
        linear 3 alpha 1.0

    show black:
        alpha 0.0
        pause 2
        linear 2.5 alpha 1.0

    stop ambient fadeout 7
    $ setWait(102.139,108.351)
    $ speak(NICOLE, "What choice do I have?")
    jump scene_0129
label scene_0067:
    $ setVoiceTrack("audio/Scenes/0067.mp3")
    scene bathroom
    show nicole sc2:
        xalign 0.265

    show crispin sc2:
        rightcenterstage
    $ setWait(0.155,2.549)
    $ speak(NICOLE, "Yes guidance counselor, let's \"talk it up\".")
    $ setWait(2.549,7.22)
    $ speak(CRISPIN, "Hey come on, no need for the jokes, I can tell you're fragile inside, me too actually.")
    $ setWait(7.22,9.598)
    $ speak(NICOLE, "Oh yeah? How can you tell?")
    $ setWait(9.598,15.687)
    $ speak(CRISPIN, "...y'know... like.. y-your face and stuff. Just how you are.")
    $ setWait(15.687,18.106)
    $ speak(NICOLE, "You've known me for literally 2 days.")
    $ setWait(18.106,20.525)
    $ speak(CRISPIN, "All I need is 2 minutes, ha ha.")
    $ setWait(20.525,24.571)
    $ speak(NICOLE, "You wanna get to the emotional part? Huffing developer's a lot more exciting than this.")
    show crispin sc2 unhappy:
        rightcenterstage
    $ setWait(24.571,35.499)
    $ speak(CRISPIN, "Look it's just, I don't know, people don't understand me. Like this girl saw I was listening to pop punk and was like \"I thought punk was anti-pop?\" like she didn't understand.")
    $ setWait(35.499,40.003)
    $ speak(NICOLE, "I would've told you the same thing, pop punk's for boring sub-urban kids who wanna live in LA.")
    $ setWait(40.003,44.716)
    $ speak(CRISPIN, "But it's deeper than that, like I feel like no one at this school gets me.")
    $ setWait(44.716,48.053)
    $ speak(NICOLE, "Just curious, were you saying that before using the internet?")
    $ setWait(48.053,51.556)
    $ speak(CRISPIN, "Man like, I don't know. There's gotta be more out there.")
    $ setWait(51.556,56.52)
    $ speak(NICOLE, "You haven't actually replied to a single thing I've said, how is this a conversation?")
    show crispin sc2:
        rightcenterstage
    $ setWait(56.52,63.36)
    $ speak(CRISPIN, "I guess it's not, huh? Not so much a conversation, more like a vent-sesh.")

    show nicole sc2:
        xalign 0.265
        linear 1 leftstage

    $ setWait(63.36,64.277)
    $ speak(NICOLE, "...Well anyway.")
    $ setWait(64.277,71.785)
    $ speak(CRISPIN, "Oh yeah yeah yeah I'll let you go now. But oh, Nicole, thanks for listening. You're a good friend and stuff.")
    stop ambient fadeout 6.5
    show black:
        alpha 0.0
        2
        linear 2 alpha 1.0
    $ setWait(71.785,78.249)
    $ speak(NICOLE, "Gee thanks, you're a good.. person I was forced to talk to.")
    jump scene_0068
label scene_0068:

    $ setVoiceTrack("audio/Scenes/0068.mp3")

    play ambient "audio/Ambience/Neighborhood_Ambience_Night.mp3" fadein 1
    scene onlayer master
    show black
    show home nicole ext night with Pause(2.038):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.038 zoom .6 truecenter

    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3"

    show nicole athome2:
        off_left
        linear 4 centerstage

    $ setWait(2.218,7.765)
    $ speak(NICOLE, "How is it $2.99 for a \"Drop It Like It's Hot\" ringtone? It's bleeps and bloops-- fuck outta here.")
    show nicole athome2 surprised:
        centerstage
    $ setWait(7.765,9.612)
    $ speak(NICOLE, "Who is this? Wait..")
    show text crispin 1
    $ setWait(9.612,12.09)
    $ speak(NICOLE, "\"Hey thanks for listening in the women's restroom\"")
    hide text crispin 1
    show nicole athome2:
        centerstage
    $ setWait(12.09,15.461)
    $ speak(NICOLE, "Oh it's that weirdo! How'd he get my number? Whatever let's see..")
    show text crispin 1
    $ setWait(15.461,19.84)
    $ speak(NICOLE, "\"I love seeing you and hearing your voice, your attitude just works for me IDK\"")
    hide text crispin 1
    $ setWait(19.841,22.281)
    $ speak(NICOLE, "Yeah IDK's real romantic..")
    show text crispin 1:
        alpha 1.0
        2.1
        alpha 0
    $ setWait(22.281,25.721)
    $ speak(NICOLE, "\"I wanted to show you what you do to me\" \n ..Show me what I don't see--")
    show nicole athome2 surprised:
        centerstage
    show text crispin 2:
        alpha 1.0
        1.2
        alpha 0
    $ setWait(25.721,30.278)
    $ speak(NICOLE, "Oh my god! All 3 inches of it! What the fuck? Why?!")

    menu:
        "DELETE AND FORGET ABOUT IT WITH THERAPY":
            jump scene_0069
        "HE MADE A MISTAKE":
            jump scene_0070
label scene_0069:
    $ setVoiceTrack("audio/Scenes/0069.mp3")
    scene home nicole int
    show nicole athome2:
        centerstage


    $ setWait(0.145,5.154)
    $ speak(NICOLE, "I'm just gonna.. erase this ugh. I was literally raped through a phone just now.")

    stop ambient fadeout 6.5

    show black:
        alpha 0.0
        3
        linear 3 alpha 1.0

    show nicole athome2:
        xzoom -1
        centerstage
        linear 4.4 off_left

    $ setWait(5.154,12.554)
    $ speak(NICOLE, "School was bad before but now I gotta deal with seeing him there.")

    show black:
        alpha 0.0
        pause 4.5
        linear 2.3 alpha 1.0

    stop ambient fadeout 7

    jump scene_0129
label scene_0070:
    $ setVoiceTrack("audio/Scenes/0070.mp3")
    scene home nicole int
    show nicole athome2 sly:
        xzoom -1
        centerstage
    $ setWait(0.161,5.886)
    $ speak(NICOLE, "Then again... he kinda just, put himself out there like that...")

    show nicole athome2 sly:
        xzoom 1

    show black:
        alpha 0.0
        3.5
        linear 2.5 alpha 1.0

    stop ambient fadeout 13

    $ setWait(5.886,16.021)
    $ speak(NICOLE, "Send it to her, send it to her, send it to him, I barely know him but let's give it to him too, send it to her...")

    show black onlayer screens:
        alpha 1.0
        0.2
        linear 2.5 alpha 0.0
    scene school int 1

    show guy_3:
        xzoom -1
        leftstage

    show girl_3:
        xzoom -1
        leftcenterstage

    show crispin sc3:
        off_right
        linear 2.7 rightcenterstage

    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 1
    $ setWait(16.321,20.859)
    $ speak(CRISPIN, "Hey guys, what's going on here we having fun? You hear the new drops at the CD shops?")
    $ setWait(20.859,22.069)
    $ speak(GUY_3, "Oh hey, Crispin.")
    show girl_3 smile:
        xzoom -1
        leftcenterstage
    $ setWait(22.069,25.614)
    $ speak(GIRL_3, "Yeah I would have but my after school time was cut kinda short..")
    show guy_3 smile:
        xzoom -1
        leftstage
    $ setWait(25.614,27.575)
    $ speak(GUY_3, "Yeah wasn't long at all, right?")
    show crispin sc3 unhappy:
        rightcenterstage
    $ setWait(27.575,29.702)
    $ speak(CRISPIN, "Aw sucks to hear bro, what happened?")
    show girl_3 laugh:
        xzoom -1
        leftcenterstage
    $ setWait(29.702,32.997)
    $ speak(GIRL_3, "Literally everyone at school's seen your micropenis.")

    show crispin sc3 unhappy:
        xzoom -1
        pause 1
        xzoom 1

    $ setWait(32.997,34.54)
    $ speak(CRISPIN, "What? No way! How?")

    show kylar sc2:
        off_right
        linear 1.3 rightstage

    show jeffery sc2:
        off_right
        pause 1.7
        linear 1 xalign 1.18
        pause 0.2
        xzoom -1
        linear 0.5 off_right

    $ setWait(34.54,38.294)
    $ speak(KYLAR, "Cause you took a picture of it ya fuckin idiot!")

    hide jeffery

    show lynn:
        off_right
        linear 1.6 xalign 0.89

    show kylar sc2:
        pause 0.8
        xzoom -1
        linear 1 off_right

    show girl_3 smile:
        xzoom -1
        leftcenterstage

    $ setWait(38.294,44.216)
    $ speak(LYNN, "Settle down! Everyone! Every week you kids get worked up over some tiny thing!")
    show girl_3 laugh:
        xzoom -1
        leftcenterstage
    $ setWait(44.216,46.468)
    $ speak(GIRL_3, "Oh you saw it too?")
    $ setWait(46.468,48.22)
    $ speak(LYNN, "What is so funny??")

    show kylar sc2:
        xzoom 1
        off_right
        linear 1.1 xalign 1.1

    $ setWait(48.22,51.807)
    $ speak(KYLAR, "Crispin's been sending out pictures of his junk to every girl in school!")

    show guy_3 smile:
        leftstage
        linear 0.7 xalign 0.1

    $ setWait(51.807,54.602)
    $ speak(GUY_3, "That's not how I heard it, I thought it was just one girl.")

    show girl_3 laugh:
        xzoom 1
        leftcenterstage

    $ setWait(54.602,57.271)
    $ speak(GIRL_3, "And then she sent it to everyone!")

    show girl_3 laugh:
        leftcenterstage
        pause 0.4
        xzoom -1

    show kylar sc2:
        xalign 1.1
        pause 1
        xzoom -1
        linear 1.5 off_right

    show guy_3 smile:
        xalign 0.1
        pause 1.5
        xzoom 1
        linear 3.2 off_farleft

    show girl_3 smile:
        leftcenterstage
        pause 1.7
        linear 3.4 off_left

    $ setWait(57.2712,60.316)
    $ speak(LYNN, "Who was it then? Tell me, Crispin!")

    hide kylar sc2

    show crispin sc3 unhappy:
        rightcenterstage
        xzoom -1
        linear 1.1 centerstage

    $ setWait(60.316,63.068)
    $ speak(CRISPIN, "The..The new girl Nicole.")

    show lynn:
        xalign 0.89
        linear 1 xalign .79

    hide girl_3
    hide guy_3

    $ setWait(63.068,68.91)
    $ speak(LYNN, "Sexually harassing our new students? You're in big trouble, mister!")
    stop ambient fadeout 2
    jump scene_0071
label scene_0071:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0071.mp3")
    scene home nicole int

    show nicole tanktop:
        xzoom -1
        leftcenterstage

    show mom 2 concerned:
        off_right
        linear 4 rightcenterstage


    play ambient "audio/Ambience/House_Night_Ambience.mp3" fadein 2
    $ setWait(0.973,5.339)
    $ speak(MOM, "Nicole, there's something we need to talk about.")

    show nicole tanktop:
        xzoom 1
        leftcenterstage

    $ setWait(5.339,7.007)
    $ speak(NICOLE, "Oh god, not you too.")
    $ setWait(7.007,13.055)
    $ speak(MOM, "Your principal called and told me there was a problem at school. A boy sent you some unsolicited pictures?")
    show nicole tanktop angry:
        leftcenterstage
    $ setWait(13.055,15.683)
    $ speak(NICOLE, "Mom, this is gross I'm not talking about it with you.")
    $ setWait(15.683,21.105)
    $ speak(MOM, "You were forced to look at sexual imagery, Nicole. The child psychologists say that can really stunt development.")
    $ setWait(21.105,25.693)
    $ speak(NICOLE, "Well everyday I'm forced to look at the Principal's fat titties just hanging out all over the god damn place.")
    $ setWait(25.693,32.908)
    $ speak(MOM, "This isn't about her-- look, I just need to know if you're okay. This was very serious.")
    menu:
        "BE HONEST WITH MOM":
            jump scene_0072
        "EXAGGERATE TRAUMA FOR PITY GIFTS":
            jump scene_0073
label scene_0072:
    $ setVoiceTrack("audio/Scenes/0072.mp3")
    scene home nicole int

    show nicole tanktop smile:
        leftcenterstage

    show mom 2 concerned:
        rightcenterstage

    $ setWait(0.112,3.507)
    $ speak(NICOLE, "Mom, I've honestly never felt better in my life.")
    $ setWait(3.507,4.842)
    $ speak(MOM, "Ugh, how?")
    $ setWait(4.842,10.848)
    $ speak(NICOLE, "Do you see the power I have here? Any guy who annoys the shit out of me I can just socially ruin.")
    $ setWait(10.848,13.976)
    $ speak(MOM, "My point is, it should have never gotten to that point.")
    show nicole tanktop angry:
        leftcenterstage
    $ setWait(13.976,15.269)
    $ speak(NICOLE, "Oh go dye your roots, Mom.")
    show mom 2 angry:
        rightcenterstage
    $ setWait(15.269,17.688)
    $ speak(MOM, "Hey, that was totally uncalled for.")
    $ setWait(17.688,24.862)
    $ speak(NICOLE, "Like I finally score a point for women and you have to have a problem with it. Other girls were talking to me like \"I'd never do that you're brave\" I'm a trendsetter, Mom!")
    show mom 2:
        rightcenterstage
    $ setWait(24.862,31.118)
    $ speak(MOM, "Ugh.. just make sure you don't provoke them too hard. Boys can be vicious, sweetie.")

    show nicole tanktop:
        leftcenterstage
        pause 1
        xzoom -1
        linear 4 off_left

    show black:
        alpha 0.0
        pause 3.6
        linear 2 alpha 1.0

    stop ambient fadeout 5

    $ setWait(31.118,38.105)
    $ speak(NICOLE, "Yeah? They haven't met me.")
    jump scene_0130
label scene_0073:
    $ setVoiceTrack("audio/Scenes/0073.mp3")
    scene home nicole int

    show nicole tanktop sad:
        leftcenterstage

    show mom 2 concerned:
        rightcenterstage

    $ setWait(0.177,3.798)
    $ speak(NICOLE, "Mom.. I really don't know. I don't think so.")

    show mom 2 concerned:
        rightcenterstage
        linear 0.8 xalign 0.58

    $ setWait(3.798,7.468)
    $ speak(MOM, "Oh sweetie what happened? It's okay, you can tell me.")
    $ setWait(7.468,8.719)
    $ speak(NICOLE, "You won't be mad?")
    $ setWait(8.719,11.097)
    $ speak(MOM, "No, you didn't do anything wrong.")
    $ setWait(11.097,16.097)
    $ speak(NICOLE, "Well, I don't know, he sent me the picture and just wouldn't stop texting me..")
    $ setWait(16.097,21.732)
    $ speak(NICOLE, "and you got the limited phone plan so I couldn't block his number. It just wouldn't stop!")
    $ setWait(21.732,25.778)
    $ speak(MOM, "Oh I'm sorry, we'll take care of that tomorrow. Now what else?")
    $ setWait(25.778,33.869)
    $ speak(NICOLE, "Well the next day at school he was way too confident with me. Just pinning me against the locker and licking my ear lobes.")
    $ setWait(33.869,36.831)
    $ speak(MOM, "That's what they fetishize now? Just sick.")
    $ setWait(36.831,42.795)
    $ speak(NICOLE, "I know! He told me I was his property and I just started crying I don't know what to do.")
    $ setWait(42.795,47.591)
    $ speak(MOM, "There there it's alright. Ooh this is the hardest part of being a Mom, I swear.")

    show nicole tanktop sad:
        leftcenterstage
        pause 6.2
        xzoom -1

    $ setWait(47.591,54.765)
    $ speak(NICOLE, "I'm sorry I'm a disappointment, Mom. I'd want a daughter who gets A's on Math tests instead of D's to the face.")

    show nicole tanktop sad:
        xzoom -1 leftcenterstage
        pause 1
        xzoom 1

    $ setWait(54.765,60.271)
    $ speak(MOM, "Stop it, I love you okay? Is there any way I can make this better? Anything at all?")

    show nicole tanktop sad:
        leftcenterstage
        xzoom 1

    $ setWait(60.271,66.443)
    $ speak(NICOLE, "Well.. maybe some new less revealing outfits, so boys stop hitting on me?")
    $ setWait(66.443,68.279)
    $ speak(MOM, "What? How many?")
    $ setWait(68.279,71.699)
    $ speak(NICOLE, "A whole wardrobe, just to get me through to graduation.")
    $ setWait(71.699,78.33)
    $ speak(MOM, "No sweetie, you can't shift your whole life around over one abuser! I'm calling the school to get him expelled!")
    $ setWait(78.33,81)
    $ speak(NICOLE, "Oh alright I guess that's fine too--")
    $ setWait(81,85.129)
    $ speak(MOM, "And if they don't, I'm filing a lawsuit, we'll even move if we have to!")
    show nicole tanktop:
        leftcenterstage
    $ setWait(85.129,87.006)
    $ speak(NICOLE, "What? Again? But I just--")

    show mom 2 concerned:
        xalign 0.58
        pause 3
        xzoom -1
        linear 3 off_right

    $ setWait(87.006,93.094)
    $ speak(MOM, "Shh! It's okay, you didn't do anything wrong. Now where's that office number?")
    stop ambient fadeout 2
    jump end_0074

label end_0074:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0074" not in persistent.endings:
        $ persistent.endings.append("end_0074")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0074end with Pause (28.7):
        alpha 1.0
    return

label scene_0075:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0075.mp3")
    play ambient "audio/Ambience/Darkroom_Ambience.mp3" fadein 0.75
    scene dark room
    show nicole sc2:
        xzoom -1
        off_right
        linear 2 rightstage


    show mr_white:
        xalign 1.2
        linear 1.8 rightcenterstage
        xzoom -1
    $ setWait(0.631,3.384)
    $ speak(MR_WHITE, "Sorry, I didn't even catch your name.")
    $ setWait(3.384,5.928)
    $ speak(NICOLE, "It's Nicole. What's yours?")
    $ setWait(5.928,10.349)
    $ speak(MR_WHITE, "You can call me Mr. White, but my friends call me Mr. Shooter!")

    show nicole sc2:
        xzoom -1 rightstage
        linear 2 leftcenterstage
        xzoom 1

    show mr_white:
        xzoom -1 rightcenterstage
        pause 1.8
        xzoom 1

    $ setWait(10.349,12.601)
    $ speak(NICOLE, "Okay, Mr. White. So what's first?")

    show nicole sc2:
        xzoom 1
        leftcenterstage

    $ setWait(12.601,19.775)
    $ speak(MR_WHITE, "Well you see Nicole, I didn't actually call you in for chemical cleaning. Needed you alone to ask something else.")
    $ setWait(19.775,20.818)
    $ speak(NICOLE, "Here it comes.")
    $ setWait(20.818,28.083)
    $ speak(MR_WHITE, "No no no, mind out of the gutter please. It's just you had a very striking look, positively pure.")
    $ setWait(28.083,36.083)
    $ speak(MR_WHITE, "I do a lot of freelance photography work outside of my teaching job here. How would you like to model for some community service hours?")
    $ setWait(36.083,40.17)
    $ speak(NICOLE, "No way I'm getting naked on camera for the community, at least $500.")
    $ setWait(40.17,44.842)
    $ speak(MR_WHITE, "Naked? No, absolutely not! You're a minor after all.")
    $ setWait(44.842,48.178)
    $ speak(NICOLE, "Oh so just wearing lingerie and baby oil, gotcha. When is it?")
    $ setWait(48.178,55.853)
    $ speak(MR_WHITE, "No, not that either. The shoot is this weekend at White Wheat Farms. Should be a nice wholesome sunny September day.")
    $ setWait(55.853,58.23)
    $ speak(NICOLE, "Okay, but the payment situation is?")
    $ setWait(58.23,60.924)
    $ speak(MR_WHITE, "You'll get a free meal of your choice.")
    menu:
        "FUCK THAT":
            jump scene_0076
        "FIND THE MOST EXPENSIVE RESTAURANT IN TOWN\nAND DO IT":
            jump scene_0077
label scene_0076:
    $ setVoiceTrack("audio/Scenes/0076.mp3")
    scene dark room

    show nicole sc2:
        leftcenterstage

    show mr_white:
        rightcenterstage

    $ setWait(0.292,5.714)
    $ speak(NICOLE, "See I feel really bad about this but sorry I can't. Your pitch was so good too.")
    $ setWait(5.714,8.425)
    $ speak(MR_WHITE, "Oh well no hard feelings, Nicole.")
    show nicole sc2 smile:
        leftcenterstage
    $ setWait(8.425,12.137)
    $ speak(NICOLE, "I'd love to make it up to you and do some cleaning in here anyway.")
    $ setWait(12.137,19.061)
    $ speak(MR_WHITE, "Aw thanks. I need to get back to my class introduction. While I'm out there, maybe you could reorganize the developers.")
    $ setWait(19.061,20.979)
    $ speak(NICOLE, "No problem, thanks.")

    show mr_white:
        rightcenterstage
        pause 1.45
        xzoom -1
        linear 1.5 off_right

    $ setWait(20.979,25.401)
    $ speak(MR_WHITE, "No; Thank you.")

    hide mr_white

    show nicole sc2:
        leftcenterstage
        linear 1.2 rightcenterstage

    stop ambient fadeout 6

    show black:
        alpha 0.0
        pause 3
        linear 3 alpha 1.0

    $ setWait(25.401,32.321)
    $ speak(NICOLE, "...Okay huffing at least one of these should get me fucked up, right?")
    jump scene_0128
label scene_0077:
    $ setVoiceTrack("audio/Scenes/0077.mp3")
    scene dark room

    show nicole sc2 smile:
        leftcenterstage

    show mr_white:
        rightcenterstage
    $ setWait(0.027,1.912)
    $ speak(NICOLE, "Y'know what? Sure.")
    $ setWait(1.912,12.297)
    $ speak(MR_WHITE, "Oh splendid! A nice pure outing, just me and my new beautiful student Nicole. I trust you'll brush up on your posing this week?")
    show nicole sc2:
        leftcenterstage
    $ setWait(12.297,14.883)
    $ speak(NICOLE, "Well I bend over to pick up the paper so shouldn't be too hard--")
    $ setWait(14.883,24.142)
    $ speak(MR_WHITE, "Then it's settled. This weekend a nice bright shoot should really cleanse our minds of the muddied culture surrounding us, don't you think?")
    $ setWait(24.142,27.896)
    $ speak(NICOLE, "Whatever you say, dude. I'll be at home Googling expensive restaurants.")
    $ setWait(27.896,33.819)
    $ speak(MR_WHITE, "And a clever girl at that. A bright mind to match your bright complexion.")

    show nicole sc2:
        leftcenterstage
        linear 3.5 off_right

    $ setWait(33.819,35.897)
    $ speak(NICOLE, "Okay bye.")
    stop ambient fadeout 2
    jump scene_0078
label scene_0078:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0078.mp3")
    play ambient "audio/Ambience/WheatField_Ambience.mp3" fadein 1.5
    scene wheat

    show mr_white:
        rightstage

    show camera:
        xalign 0.75

    show nicole white:
        leftstage

    $ setWait(1.669,11.554)
    $ speak(MR_WHITE, "That's it.. wonderful. Your pure skin just wonderfully fades out into the highlights of the wheat behind you.")
    $ setWait(11.554,16.726)
    $ speak(NICOLE, "Yeah thanks, could you talk about something other than skin? It's like a dermatology fever dream.")
    $ setWait(16.726,25.86)
    $ speak(MR_WHITE, "Sorry, Nicole. When something catches my eye I just can't let it go. The curse of being a photographer.")
    $ setWait(25.86,31.073)
    $ speak(NICOLE, "Okay, so what's this thing on my shirt again? The Celtics logo or something?")
    $ setWait(31.073,40.791)
    $ speak(MR_WHITE, "No no, the Celtic cross. Just a graphic rich with heritage to compliment the nice wholesome imagery behind you.")
    $ setWait(40.791,43.836)
    $ speak(NICOLE, "Whatever you say.. so are we done yet?")
    $ setWait(43.836,48.424)
    $ speak(MR_WHITE, "And.. Yes we are! It was a pleasure, Nicole.")
    $ setWait(48.424,52.386)
    $ speak(NICOLE, "The pleasure was all yours. So there's a steakhouse on the other side of town and--")

    show mr_white:
        rightstage
        pause 3.2
        linear 3.5 leftcenterstage

    $ setWait(52.386,63.355)
    $ speak(MR_WHITE, "Yes yes, I'll hold up my end of the deal, don't worry. But before we leave I just wanted to ask you.. Do you enjoy being white?")

    show mr_white:
        leftcenterstage

    $ setWait(63.355,66.984)
    $ speak(NICOLE, "I mean, not sure how white I'll be after standing in this sun all day.")
    $ setWait(66.984,76.368)
    $ speak(MR_WHITE, "No sorry, allow me to rephrase the question.. Do you love the white American culture? Are you a proud white woman?")
    menu:
        "QUESTION HIS QUESTIONS":
            jump scene_0079
        "FAKE YES TO GET FREE FOOD FASTER":
            jump scene_0080
label scene_0079:
    $ setVoiceTrack("audio/Scenes/0079.mp3")
    scene wheat

    show nicole white:
        leftstage

    show camera:
        xalign 0.75

    show mr_white:
        leftcenterstage

    $ setWait(0.354,4.508)
    $ speak(NICOLE, "Like.. No? Yes? Who cares? Why are you so into whiteness?")
    $ setWait(4.508,13.976)
    $ speak(MR_WHITE, "Sorry, I guess the questions have been a tad much. There's just something about the color white, and it's not just my last name.")
    $ setWait(13.976,16.186)
    $ speak(NICOLE, "White's a pretty boring color to be honest.")
    $ setWait(16.186,23.786)
    $ speak(MR_WHITE, "I wouldn't call it boring, just.. pure. You're a photography student, think of it like a camera.")
    $ setWait(23.786,38.25)
    $ speak(MR_WHITE, "When you take the lens off and snap a picture, the image is just white. Then you put it back on and focus, the shapes seen are merely obstructions, sullying the whiteness.")
    $ setWait(38.25,40.21)
    $ speak(NICOLE, "What the fuck does this have to do with anything?")
    $ setWait(40.21,56.06)
    $ speak(MR_WHITE, "It's just a metaphor for a larger problem in this country. We focus on other cultural obstructions so much that we've allowed them to mix with and tarnish the initial whiteness that started it all.")
    $ setWait(56.06,64.777)
    $ speak(NICOLE, "Huh.. yeah I think I might get it, but could you give an example of a \"cultural obstruction\"")
    $ setWait(64.777,67.237)
    $ speak(MR_WHITE, "Rap music.")
    show nicole white:
        leftstage
    $ setWait(67.237,69.198)
    $ speak(NICOLE, "Huh...")
    stop ambient fadeout 1.5
    jump scene_0081
label scene_0080:
    $ setVoiceTrack("audio/Scenes/0080.mp3")
    scene wheat

    show nicole white:
        leftstage

    show mr_white:
        leftcenterstage

    show camera:
        xalign 0.75

    $ setWait(0.227,3.33)
    $ speak(NICOLE, "Yeah, totally love it. A lot actually, can we go now?")
    $ setWait(3.33,9.294)
    $ speak(MR_WHITE, "Oh that's wonderful to hear, I trust your heritage is important to you as well?")
    $ setWait(9.294,11.379)
    $ speak(NICOLE, "If I knew what it was then absolutely.")
    $ setWait(11.379,19.596)
    $ speak(MR_WHITE, "So great to find a like-minded student in my class. I love our race and I'm proud of it! This is the first shoot of many, Nicole!")
    $ setWait(19.596,21.723)
    $ speak(NICOLE, "Cool, will I get paid next time?")
    $ setWait(21.723,25.393)
    $ speak(MR_WHITE, "How would you like 50 dollars a shoot? It adds up!")
    $ setWait(25.393,27.604)
    $ speak(NICOLE, "Sweet yeah, anytime any place.")
    $ setWait(27.604,33.693)
    $ speak(MR_WHITE, "Now that I know you're on board for the racial purification of this country, you deserve it!")
    show nicole white surprised:
        leftstage
    $ setWait(33.693,35.504)
    $ speak(NICOLE, "...Oh.")

    stop ambient fadeout 1.5
    jump scene_0081
label scene_0081:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0081.mp3")
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 2
    scene cafeteria int

    show nicole sc3:
        leftcenterstage

    show jecka sc3 unhappy:
        rightcenterstage

    $ setWait(0.1,3.915)
    $ speak(NICOLE, "")
    $ setWait(3.915,9.22)
    $ speak(NICOLE, "...So I'm pretty sure the photography teacher's a white nationalist.")
    $ setWait(9.22,13.391)
    $ speak(JECKA, "...I said \"the tuna's good today\" and you just replied with that.")
    $ setWait(13.391,15.893)
    $ speak(NICOLE, "Remember how I told you I did that photoshoot with him?")
    show jecka sc3 angry:
        rightcenterstage
    $ setWait(15.893,17.395)
    $ speak(JECKA, "Yes, please brag again.")
    show jecka sc3 unhappy:
        rightcenterstage

    $ setWait(17.395,24.652)
    $ speak(NICOLE, "No it's not that, just the whole time he was saying this weird shit about whiteness and being white.")
    $ setWait(24.652,28.406)
    $ speak(JECKA, "I guess it fits, Mr. White's a white supremacist.")
    $ setWait(28.406,29.865)
    $ speak(NICOLE, "White nationalist.")
    $ setWait(29.865,31.325)
    $ speak(JECKA, "Isn't it the same thing?")
    $ setWait(31.325,37.957)
    $ speak(NICOLE, "White supremacists assume white culture is the correct culture. White nationalists politicize that.")
    $ setWait(37.957,40.459)
    $ speak(JECKA, "So.. he's?")
    $ setWait(40.459,44.88)
    $ speak(NICOLE, "Mr. White is a white nationalist. Pretty much everyone who goes here is a white supremacist.")
    $ setWait(44.88,47.758)
    $ speak(JECKA, "Oh, that makes sense.")
    show nicole sc3 sly:
        leftcenterstage
    $ setWait(47.758,49.302)
    $ speak(NICOLE, "Does it?")
    show jecka sc3 worried:
        rightcenterstage
    $ setWait(49.302,51.22)
    $ speak(JECKA, "...Am I racist if I say no?")
    show nicole sc3 sly:
        leftcenterstage
    $ setWait(51.22,54.515)
    $ speak(NICOLE, "Honestly I don't give a shit, that's just what Google told me last night.")
    show jecka sc3 unhappy:
        rightcenterstage
    $ setWait(54.515,58.426)
    $ speak(JECKA, "Well if we have some KKK guy at our school shouldn't we do something?")
    show nicole sc3:
        leftcenterstage
    $ setWait(58.426,65.2)
    $ speak(NICOLE, "Like what? Even if we told someone they won't do anything. If being racist got you fired like no one would have a job.")
    $ setWait(65.2,74.71)
    $ speak(JECKA, "Well I'm kinda curious now. I think I'll go up and see what he's all about. Maybe catch him on something else. You coming with me? He knows you, right?")

    stop ambient fadeout 1.7
    menu:
        "NON-RACIST GIRLS GOTTA STICK TOGETHER":
            jump scene_0082
        "I'D RATHER SEE IF THE JANITOR'S SELLING XANAX":
            jump scene_0084
label scene_0082:

    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0

    $ setVoiceTrack("audio/Scenes/0082.mp3")
    play ambient "audio/Ambience/Darkroom_Ambience.mp3" fadein 1
    scene dark room

    show mr_white:
        xzoom -1 leftcenterstage

    show nicole sc3:
        off_farright
        xzoom -1
        linear 2.4 rightstage

    show jecka sc3 angry:
        off_right
        linear 2 rightcenterstage

    $ setWait(0.661,8.377)
    $ speak(MR_WHITE, "What a lovely surprise, girls. Now Nicole, you wouldn't happen to be recruiting another loyal white to our cause?")

    show jecka sc3 worried:
        xalign 0.77
        xzoom -1

    $ setWait(8.377,12.673)
    $ speak(JECKA, "Oh my god it is true. We didn't even work it out of him or anything.")
    $ setWait(12.673,14.8)
    $ speak(NICOLE, "Really puts the proud in \"white pride\".")

    show jecka sc3 angry:
        xalign 0.77
        xzoom -1
        pause 0.5
        rightcenterstage
        xzoom 1

    $ setWait(14.8,21.14)
    $ speak(MR_WHITE, "Judging by your tones, I'm starting to think neither of you are down for the purification of this nation.")
    $ setWait(21.14,22.015)
    $ speak(NICOLE, "No shit.")
    $ setWait(22.015,26.603)
    $ speak(JECKA, "Is that why you're teaching here? To convert quirky art girls into Klan members?")
    $ setWait(26.603,34.987)
    $ speak(MR_WHITE, "Well when you put it that way it sounds too easy. The art school girls are absolutely terrified of black people, not that there's anything wrong with that.")
    show nicole sc3 surprised:
        xzoom -1
        rightstage
    $ setWait(34.987,36.697)
    $ speak(NICOLE, "You really think I'm a quirky art girl?")

    show nicole sc3:
        xzoom -1
        rightstage

    show jecka sc3 unhappy:
        rightcenterstage
        xzoom -1

    $ setWait(36.697,38.49)
    $ speak(JECKA, "No it's just a broad example.")

    show jecka sc3 unhappy:
        rightcenterstage
        xzoom 1

    $ setWait(38.49,48.50)
    $ speak(MR_WHITE, "Please just try to see this my way. The White Pride Party's understood the errors of their ways in the 20th century. Since then it's evolved from arson and lynchings.")
    $ setWait(48.50,56.341)
    $ speak(MR_WHITE, "We simply wish to promote pride in our own heritage, just like the colored communities do.")
    $ setWait(56.341,57.801)
    $ speak(NICOLE, "Colored communities?")
    $ setWait(57.801,60.512)
    $ speak(MR_WHITE, "Oh, I'm sorry, people of color.")
    $ setWait(60.512,61.555)
    $ speak(JECKA, "How is that better?")
    $ setWait(61.555,66.143)
    $ speak(MR_WHITE, "So there's black pride, that's fine. How is white pride any different?")
    $ setWait(66.143,69.73)
    $ speak(NICOLE, "Proud about what? You already own everything, it's just a victory lap.")
    show jecka sc3 angry:
        rightcenterstage
    $ setWait(69.73,72.316)
    $ speak(JECKA, "If you don't cut this shit out we're gonna stop it.")
    $ setWait(72.316,78.655)
    $ speak(MR_WHITE, "You're two little teenage girls, you have no power over me or my people.")
    $ setWait(78.655,81.783)
    $ speak(JECKA, "Maybe not, but the principal does! Let's go!")

    show jecka sc3 angry:
        xzoom -1
        rightcenterstage
        linear 0.9 off_right

    show nicole sc3:
        xzoom 1
        rightstage
        linear 1 off_farright

    $ setWait(81.783,84.953)
    $ speak(NICOLE, "Ugh, did not wanna get this involved.")
    $ setWait(84.953,88.54)
    $ speak(MR_WHITE, "Go ahead and try.")

    stop ambient fadeout 2
    jump scene_0083
label scene_0083:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0083.mp3")
    scene office 2
    show lynn:
        xzoom -1 rightstage
    play ambient "audio/ambience/office_ambience.mp3" fadein 1
    $ setWait(0.29,2.667)
    $ speak(LYNN, "If you looked like me you'd cheat on your husband too.")

    show jecka sc3 angry:
        xzoom -1
        off_left
        linear 1 leftcenterstage

    show nicole sc3:
        off_farleft
        linear 1.5 leftstage

    show lynn:
        pause 1.5
        xzoom 1

    $ setWait(2.667,5.587)
    $ speak(JECKA, "Miss Lynn! Sorry but this is kind of important!")

    show lynn:
        xzoom -1
    $ setWait(5.587,10.425)
    $ speak(LYNN, "Hey, yeah, I'll call you back. You'll get the number for lip injections after, kay bye.")
    $ setWait(10.425,13.428)
    $ speak(NICOLE, "You do illegal plastic surgery out of your basement or something?")

    show jecka sc3:
        xzoom -1
        leftcenterstage

    show lynn:
        rightstage
        xzoom 1
        pause 1
        linear 1 rightcenterstage

    $ setWait(13.428,15.805)
    $ speak(LYNN, "No, my friend does. How can I help you girls?")
    $ setWait(15.805,18.141)
    $ speak(JECKA, "It's about Mr. White in Photography. He's kinda--")
    $ setWait(18.141,22.312)
    $ speak(LYNN, "Stop, stop. I get this conversation once a year.")
    show jecka sc3 surprised:
        leftcenterstage
    $ setWait(22.312,24.189)
    $ speak(JECKA, "You've known about this?")
    $ setWait(24.189,26.024)
    $ speak(LYNN, "Unfortunately.")
    show jecka sc3 angry:
        leftcenterstage
    $ setWait(26.024,27.525)
    $ speak(JECKA, "And you're just okay with it?")
    $ setWait(27.525,32.238)
    $ speak(LYNN, "Absolutely not but his defenses have my hands tied I'm afraid.")
    $ setWait(32.238,33.156)
    $ speak(JECKA, "It's sick.")
    $ setWait(33.156,44.125)
    $ speak(LYNN, "I'd be inclined to agree. Another level of twisted, but he's made very strong cases for covering himself in peanut butter to pose for the students so I'd rather not push the issue further.")
    show jecka sc3 unhappy:
        leftcenterstage
    $ setWait(44.125,46.127)
    $ speak(NICOLE, "...What the fuck are you talking about?")
    $ setWait(46.127,48.213)
    $ speak(LYNN, "Oh.. This isn't about that?")
    $ setWait(48.213,53.635)
    $ speak(JECKA, "We're here to report he's trying to recruit his students for white nationalism rallies?")
    $ setWait(53.635,55.178)
    $ speak(LYNN, "Okay this I didn't know about.")
    $ setWait(55.178,61.684)
    $ speak(NICOLE, "Yeah he asked me to pose for a weekend shoot and kept going on about how racially pure my skin was.")
    $ setWait(61.684,63.686)
    $ speak(LYNN, "You had your clothes on, right?")
    $ setWait(63.686,64.854)
    $ speak(NICOLE, "..Why wouldn't I?")
    $ setWait(64.854,66.189)
    $ speak(LYNN, "No reason, go ahead.")
    $ setWait(66.189,71.778)
    $ speak(JECKA, "So we talked to him in the darkroom and he's just outwardly trying to sell us on white pride.")
    $ setWait(71.778,78.743)
    $ speak(LYNN, "Oh man, uh. Well that is cause for concern... Were any racial slurs used?")
    $ setWait(78.743,81.913)
    $ speak(NICOLE, "Not really, but it's more like the overall content--")
    $ setWait(81.913,83.581)
    $ speak(LYNN, "I'm afraid I can't help you then.")
    $ setWait(83.581,84.249)
    $ speak(JECKA, "What!?")
    $ setWait(84.249,95.802)
    $ speak(LYNN, "For a claim like that you'd need pretty hard evidence to get him removed from the faculty entirely... Also he may or may not have rather compromising photographs of me so I'd rather not get involved.")
    $ setWait(95.802,101.182)
    $ speak(NICOLE, "He may or may not have pictures of you in Neo Nazi shirts? Cause I may or may not have been there.")
    $ setWait(101.182,104.477)
    $ speak(LYNN, "Actually, I may or may not have been covered in baby oil.")
    show jecka sc3 angry:
        leftcenterstage
        xzoom -1
    $ setWait(104.477,108.69)
    $ speak(JECKA, "Ugh.. well I guess racism wins.")
    $ setWait(108.69,109.816)
    $ speak(NICOLE, "..Can we see the pictures?")

    show black:
        alpha 0.0
        pause 1
        linear 2.5 alpha 1.0

    stop ambient fadeout 5

    show nicole sc3:
        pause 1.4
        leftstage
        xzoom -1
        linear 2.5 off_farleft

    show jecka sc3 unhappy:
        pause 1.4
        leftcenterstage
        xzoom 1
        linear 2.1 off_left

    $ setWait(109.816,114.659)
    $ speak(LYNN, "Get out of my office.")
    jump scene_0129
label scene_0084:
    $ setVoiceTrack("audio/Scenes/0084.mp3")

    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 0.7
    scene cafeteria int

    show nicole sc3:
        leftcenterstage

    show jecka sc3 unhappy:
        rightcenterstage

    $ setWait(0.181,4.385)
    $ speak(NICOLE, "Dude I really don't wanna get involved. You're smart enough you can handle it.")
    $ setWait(4.385,8.597)
    $ speak(JECKA, "Are you saying that cause you really mean it or just cause you don't wanna go?")
    $ setWait(8.597,9.64)
    $ speak(NICOLE, "Can it be both?")
    show jecka sc3 angry:
        rightcenterstage
    $ setWait(9.64,10.974)
    $ speak(JECKA, "You're such a bitch.")
    $ setWait(10.974,14.978)
    $ speak(NICOLE, "How? Cause I don't wanna see a white nationalist more than I already have to?")
    $ setWait(14.978,20.192)
    $ speak(JECKA, "You got me all worked up over this and you won't even dig into it with me. What kinda friend are you?")
    $ setWait(20.192,21.61)
    $ speak(NICOLE, "I've known you for like a week.")
    $ setWait(21.61,26.156)
    $ speak(JECKA, "We're the only 2 pretty girls in this lunch block we're gonna end up best friends anyway.")
    $ setWait(26.156,29.284)
    $ speak(NICOLE, "And that right there is why your loyalty check isn't working.")
    show jecka sc3 unhappy:
        rightcenterstage
    $ setWait(29.284,32.371)
    $ speak(JECKA, "Whatever fine. See you after school?")
    $ setWait(32.371,38.21)
    $ speak(NICOLE, "Yeah may as well. I actually have some counselor meeting for new student integration.")
    show jecka sc3 worried:
        rightcenterstage
    $ setWait(38.21,40.504)
    $ speak(JECKA, "Oh good luck with that.")
    $ setWait(40.504,42.548)
    $ speak(NICOLE, "Why are you saying it like that?")

    show jecka sc3 unhappy:
        rightcenterstage
        pause 2.2
        xzoom -1
        linear 3 off_right

    show nicole sc3:
        leftcenterstage
        pause 4.5
        xzoom -1
        linear 3 off_left

    $ setWait(42.548,47.052)
    $ speak(JECKA, "The counselor is.. well you'll see.")
    stop ambient fadeout 1.5
    jump scene_0085
label scene_0085:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0085.mp3")
    scene office 1
    show nicole sc3:
        centerstage

    show couns smile:
        rightstage
    play ambient "audio/ambience/office_ambience.mp3" fadein 1.5
    $ setWait(0.467,7.173)
    $ speak(COUNSELOR, "See, Nicole? Doesn't it just feel great to openly talk about sex in a safe environment?")
    $ setWait(7.173,12.512)
    $ speak(NICOLE, "No actually, not at all. Aren't you supposed to be asking me if I'm making friends or something?")
    $ setWait(12.512,23.732)
    $ speak(COUNSELOR, "Eh, same old same old. I prefer a different approach, really getting into the dramatic psyche of our students. At your age, it's the number one thing on your mind.")
    $ setWait(23.732,27.736)
    $ speak(NICOLE, "Talking about sex with a man 20 years older than me is the first thing on my mind?")
    $ setWait(27.736,32.866)
    $ speak(COUNSELOR, "Merely a societal taboo. A social construct if anything.")
    $ setWait(32.866,33.867)
    $ speak(NICOLE, "Huh?")
    $ setWait(33.867,43.367)
    $ speak(COUNSELOR, "Take homophobia for example, that brand of hatred was brought on by other people. Nothing intrinsically wrong with homosexuality.")
    $ setWait(43.367,49.632)
    $ speak(COUNSELOR, "But then what's the next taboo to be lifted? Let's say if you and me dated outside of school.")
    $ setWait(49.632,50.633)
    $ speak(NICOLE, "Here we go.")
    $ setWait(50.633,65.398)
    $ speak(COUNSELOR, "Perhaps in our lifetime, a relationship with someone of my age and someone of yours wouldn't be so frowned upon. At the end of the day, love has no boundaries. Does that make sense, are you dialed in here?")
    $ setWait(65.398,67.317)
    $ speak(NICOLE, "I'm about to dial 911.")
    $ setWait(67.317,69.36)
    $ speak(COUNSELOR, "Nonsense, what's wrong?")
    menu:
        "CALL OUT HIS\nPEDOPHILOSOPHY":
            jump scene_0086
        "TALK ABOUT SOMETHING WAY COOLER":
            jump scene_0087
label scene_0086:
    $ setVoiceTrack("audio/Scenes/0086.mp3")
    scene office 1

    show nicole sc3:
        centerstage

    show couns smile:
        rightstage
    $ setWait(0.185,5.749)
    $ speak(NICOLE, "You work at a school and you're giving me the \"age is just a number\" speech. Shouldn't you do that on your court date?")
    $ setWait(5.749,7.834)
    $ speak(COUNSELOR, "Sorry I don't play tennis.")
    $ setWait(7.834,8.961)
    $ speak(NICOLE, "Hilarious.")
    $ setWait(8.961,16.176)
    $ speak(COUNSELOR, "Perhaps you're just not ready for an adult conversation. You're still growing after all, blooming as a young woman.")
    $ setWait(16.176,19.513)
    $ speak(NICOLE, "Yeah so I'm off limits. Are we done here?")
    $ setWait(19.513,30.482)
    $ speak(COUNSELOR, "Well, one last food for thought. Your driver's license may say you're still a girl, but your body knows you're a woman right now. Prime for reproduction.")
    $ setWait(30.482,32.401)
    $ speak(NICOLE, "What? Cause I have a period?")
    $ setWait(32.401,38.407)
    $ speak(COUNSELOR, "Not to get graphic but, yes. Nothing wrong with that, it's natural.")
    $ setWait(38.407,40.659)
    $ speak(NICOLE, "So I should've had a baby at 13 then?")
    $ setWait(40.659,45.68)
    $ speak(COUNSELOR, "No just intercourse at 13, the baby coming by the time you're 14.")

    show nicole sc3 surprised:
        xzoom -1
        centerstage
        linear 2.5 off_left

    $ setWait(45.68,46.832)
    $ speak(NICOLE, "I'm leaving.")

    show couns:
        rightstage
        linear 1.5 rightcenterstage

    stop ambient fadeout 9

    $ setWait(46.832,54.131)
    $ speak(COUNSELOR, "Theoretically of course! ..Hm.. If she tells her parents I'll just say she was acting out.")

    jump scene_0088
label scene_0087:
    $ setVoiceTrack("audio/Scenes/0087.mp3")
    scene office 1

    show nicole sc3:
        centerstage

    show couns smile:
        rightstage
    $ setWait(0.196,4.625)
    $ speak(NICOLE, "Uh.. Nothing nevermind-- Have you heard Comeback Season?")
    $ setWait(4.625,5.96)
    $ speak(COUNSELOR, "Comeback Season?")
    $ setWait(5.96,9.046)
    $ speak(NICOLE, "It's that new mixtape from the actor rapper guy.")
    $ setWait(9.046,16.136)
    $ speak(COUNSELOR, "Oh sounds \"cool\"! Always important to be in tune with the music you kids listen to.")
    $ setWait(16.136,22.726)
    $ speak(NICOLE, "Right. Well I need to go.. meditate to it, I'll see ya later. Great talk by the way.")
    $ setWait(22.726,29.066)
    $ speak(COUNSELOR, "Oh and same to you. I love a young woman who isn't afraid to challenge societal norms!")

    show nicole sc3:
        centerstage
        linear 0.8 leftcenterstage
        pause 0.4
        xzoom -1
        linear 1 off_left

    $ setWait(29.066,30.901)
    $ speak(NICOLE, "Yeah whatever bye.")

    stop ambient fadeout 1
    jump scene_0088
label scene_0088:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0088.mp3")
    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 1.5
    scene school int 2

    show nicole sc3:
        off_left
        linear 3 leftcenterstage

    show jecka sc3:
        rightstage
        linear 1.5 rightcenterstage
    $ setWait(0.798,2.758)
    $ speak(JECKA, "Oh hey, was wondering where you were.")
    $ setWait(2.758,5.803)
    $ speak(NICOLE, "Yeah the counselor had me held up in there for a while.")
    show jecka sc3 worried:
        rightcenterstage
    $ setWait(5.803,8.055)
    $ speak(JECKA, "He didn't.. uh?")
    $ setWait(8.055,10.349)
    $ speak(NICOLE, "Defend pedophilia? He absolutely did.")
    show jecka sc3 unhappy:
        rightcenterstage
    $ setWait(10.349,13.186)
    $ speak(JECKA, "Yeah he does that.. someone should say something, right?")
    $ setWait(13.186,18.691)
    $ speak(NICOLE, "I would but then I have to fill out paperwork and honestly they have me write enough in this place as it is.")
    $ setWait(18.691,20.401)
    $ speak(JECKA, "I know, yeah.")
    $ setWait(20.401,23.571)
    $ speak(NICOLE, "So how'd things go with Mr. White?")
    show jecka sc3 worried:
        rightcenterstage
    $ setWait(23.571,34.582)
    $ speak(JECKA, "Uh, okay yeah about that. So I was talking to him, kinda confronting him, and his arguments weren't.. that.. out there.")
    $ setWait(34.582,38.294)
    $ speak(NICOLE, "I don't get it, he's a political extremist, how is he not out there?")
    show jecka sc3 unhappy:
        rightcenterstage
    $ setWait(38.294,50.306)
    $ speak(JECKA, "See we said that but like.. He asked me why it's okay to do black pride and Mexican pride but not white pride, and I really didn't have an answer for him.")
    $ setWait(50.306,53.476)
    $ speak(NICOLE, "So you just kinda backed off then?")
    $ setWait(53.476,63.945)
    $ speak(JECKA, "Well not exactly. I kept asking more and more about it, and we actually agreed on a lot. He wants me to do a shoot with him this weekend for the White Pride Party's blog.")
    $ setWait(63.945,65.613)
    $ speak(NICOLE, "..And what'd you tell him?")
    show jecka sc3:
        rightcenterstage
    $ setWait(65.613,71.827)
    $ speak(JECKA, "I said \"absolutely\"! Nothing wrong with being proud of your heritage, why not? Plus 50 bucks for the day.")
    $ setWait(71.827,74.33)
    $ speak(NICOLE, "Did he mention an ethnostate for white people?")
    $ setWait(74.33,82.129)
    $ speak(JECKA, "He might've briefly gone into it, Mr. White kept telling me how pretty my skin was I wasn't paying attention. What's an ethnostate anyway?")
    $ setWait(82.129,90.137)
    $ speak(NICOLE, "A country where all the non-white races are kinda exterminated.")
    $ setWait(90.137,95.101)
    $ speak(JECKA, "Oh it's probably not even that serious. All I know is I'm proud to be white!")
    stop ambient fadeout 2
    menu:
        "AGREE TO DISAGREE LIKE A FENCE-SITTING LIBERAL":
            jump scene_0089
        "HMM MAYBE IT'S NOT SO BAD AFTER ALL":
            jump scene_0090
label scene_0089:
    $ setVoiceTrack("audio/Scenes/0089.mp3")
    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 0.5
    scene school int 2
    show nicole sc3:
        leftcenterstage

    show jecka sc3:
        rightcenterstage
    $ setWait(0.412,6.543)
    $ speak(NICOLE, "You know what, forget it, just do what you want. I'd rather have a white nationalist lunch friend than no friend at all.")
    $ setWait(6.543,10.923)
    $ speak(JECKA, "Nicole, you rock. We can't let some silly politics get in the way of us, right?")
    $ setWait(10.923,14.051)
    $ speak(NICOLE, "Yeah sure, it's not worth getting worked up over.")

    show jecka sc3:
        rightcenterstage
        linear 3.3 off_left

    show nicole sc3:
        pause 1.5
        xzoom -1

    $ setWait(14.051,17.304)
    $ speak(JECKA, "Cool, I'll see you at lunch tomorrow. Bye!")
    stop ambient fadeout 2
    jump scene_0092
label scene_0090:
    $ setVoiceTrack("audio/Scenes/0090.mp3")
    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 0.5
    scene school int 2
    show nicole sc3 smile:
        leftcenterstage

    show jecka sc3:
        rightcenterstage
    $ setWait(0.217,8.675)
    $ speak(NICOLE, "I mean I guess when you think about it, it is kinda silly to tell just one group they can't be proud.")
    $ setWait(8.675,11.845)
    $ speak(JECKA, "Exactly, like isn't that racism in itself?")
    $ setWait(11.845,13.18)
    $ speak(NICOLE, "I get where you're coming from.")
    $ setWait(13.18,20.187)
    $ speak(JECKA, "See? He's not so bad. Hey, you should come to the shoot with me. We can make it a social thing for a good cause, y'know?")
    $ setWait(20.187,23.607)
    $ speak(NICOLE, "This weekend? ..Yeah I guess I could do another shoot.")
    $ setWait(23.607,29.279)
    $ speak(JECKA, "Awesome yeah it'll be fun. He'll fill us in on his whole solution for race relations and everything.")
    $ setWait(29.279,31.323)
    $ speak(NICOLE, "His ethnostate solution?")
    $ setWait(31.323,36.536)
    $ speak(JECKA, "Maybe, but who cares? If black people get February we could at least get California.")
    $ setWait(36.536,38.497)
    $ speak(NICOLE, "You think all the white people would fit there?")
    $ setWait(38.497,44.878)
    $ speak(JECKA, "If not then Washington and Oregon too. Minorities still have another 47 states to pick from anyway.")
    $ setWait(44.878,46.88)
    $ speak(NICOLE, "That's a good point. See ya this weekend.")


    show jecka sc3:
        rightcenterstage
        xzoom -1
        linear 3 off_right

    $ setWait(46.88,48.715)
    $ speak(JECKA, "White power!")
    stop ambient fadeout 2
    jump end_0091

label end_0091:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0091" not in persistent.endings:
        $ persistent.endings.append("end_0091")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0091end with Pause (49.6):
        alpha 1.0
    return

label scene_0092:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0092.mp3")
    play ambient "audio/Ambience/Classroom_Ambience.mp3" fadein 1
    scene classroom int 3
    show teacher_2:
        rightstage

    show nicole sc4:
        leftstage

    show girl_4:
        xzoom -1
        rightcenterstage

    show guy_2:
        xzoom -1
        leftcenterstage


    $ setWait(0.967,6.556)
    $ speak(TEACHER_2, "Who can tell me who our 3rd president was? Show of hands... Yes?")

    show girl_4:
        rightcenterstage
        linear 0.5 xalign .75

    $ setWait(6.556,7.724)
    $ speak(GIRL_4, "Thomas Jefferson?")

    show girl_4:
        xalign .75
        pause 1
        linear 0.6 rightcenterstage


    $ setWait(7.724,13.104)
    $ speak(TEACHER_2, "Very good. One of the more interesting presidents of the 19th century for a variety of reasons.")

    show kylar sc3:
        xzoom -1
        off_left
        linear 0.6 xalign -.17

    $ setWait(13.104,15.523)
    $ speak(KYLAR, "Yeah he had sex with slaves, gross!")

    show kylar sc3:
        xalign -.17
        linear 1 off_left

    $ setWait(15.523,22.989)
    $ speak(TEACHER_2, "Quiet down! Now, who can tell me Jefferson's biggest achievement?\n\n...No hands? okay Nicole.")
    $ setWait(22.989,23.907)
    $ speak(NICOLE, "Huh?")
    $ setWait(23.907,29.954)
    $ speak(TEACHER_2, "No I'm sorry \"huh\" was not one of his achievements, you were close though.")
    $ setWait(29.954,31.581)
    $ speak(NICOLE, "You hear how no one's laughing?")
    $ setWait(31.581,34.751)
    $ speak(TEACHER_2, "Just answer the question, at least try.")
    $ setWait(34.751,35.877)
    $ speak(NICOLE, "What was it again?")
    $ setWait(35.877,38.588)
    $ speak(TEACHER_2, "Thomas Jefferson's biggest achievement, what was it?")
    menu:
        "I DON'T KNOW":
            jump scene_0093
        "WHO GIVES A SHIT":
            jump scene_0094
label scene_0093:
    $ setVoiceTrack("audio/Scenes/0093.mp3")
    scene classroom int 3
    show teacher_2:
        rightstage

    show nicole sc4:
        leftstage

    show girl_4:
        xzoom -1
        rightcenterstage

    show guy_2:
        xzoom -1
        leftcenterstage
    $ setWait(0.222,1.706)
    $ speak(NICOLE, "Sorry, couldn't tell ya.")
    $ setWait(1.706,3.416)
    $ speak(TEACHER_2, "Come on, you didn't even try.")
    $ setWait(3.416,7.17)
    $ speak(NICOLE, "Did it have something to do with the slave sex thing he said?")
    $ setWait(7.17,9.047)
    $ speak(TEACHER_2, "No, please stay on subject.")
    $ setWait(9.047,18.765)
    $ speak(NICOLE, "Cause when you think about it he's the first president to have an interracial relationship. That might make him the least racist president of all time until Obama gets elected.")
    show girl_4:
        xzoom 1
    $ setWait(18.765,20.725)
    $ speak(GIRL_4, "He literally owned slaves.")

    $ setWait(20.725,24.771)
    $ speak(NICOLE, "Obama owned slaves? I guess we'll never have a non-racist president.")
    $ setWait(24.771,27.023)
    $ speak(GIRL_4, "Uh no, Thomas Jefferson.")

    show girl_4:
        rightcenterstage
        pause 2.65
        linear 4 off_left

    show guy_2:
        pause 2.65
        leftcenterstage
        xzoom 1
        linear 3 off_left

    $ setWait(27.023,30.36)
    $ speak(NICOLE, "Uh yeah, I was joking.")

    show teacher_2:
        rightstage
        linear 2.2 rightcenterstage

    $ setWait(30.36,33.321)
    $ speak(TEACHER_2, "Thank you for derailing yet another class, Nicole.")

    show nicole sc4:
        leftstage
        pause 1.3
        xzoom -1
        linear 2.2 off_left

    $ setWait(33.321,37.067)
    $ speak(NICOLE, "Tell that to Lacrosse kid, he said the slave shit first.")
    stop ambient fadeout 2
    jump scene_0095
label scene_0094:
    $ setVoiceTrack("audio/Scenes/0094.mp3")
    scene classroom int 3
    show teacher_2:
        rightstage

    show nicole sc4:
        leftstage

    show girl_4:
        xzoom -1
        rightcenterstage

    show guy_2:
        xzoom -1
        leftcenterstage
    $ setWait(0.258,1.543)
    $ speak(NICOLE, "Who gives a shit?")
    $ setWait(1.543,2.961)
    $ speak(TEACHER_2, "Ugh... what?")
    $ setWait(2.961,7.549)
    $ speak(NICOLE, "Is that the first time you ever heard that? You can't force me to care about any of this.")
    $ setWait(7.549,10.301)
    $ speak(TEACHER_2, "You'll care when your SAT scores come back!")
    $ setWait(10.301,14.973)
    $ speak(NICOLE, "I'm not taking the SATs, you only need that if you're going to a 4 year college.")

    show teacher_2:
        rightstage
        linear 0.7 xalign 0.86

    $ setWait(14.973,18.434)
    $ speak(TEACHER_2, "Oh so you're not going to college then? Think you have it all figured out?")

    show guy_2:
        leftcenterstage
        pause 3.55
        xzoom 1
        linear 3 off_left

    show girl_4:
        rightcenterstage
        pause 3.8
        xzoom 1
        linear 4 off_left


    $ setWait(18.434,23.815)
    $ speak(NICOLE, "Why would a girl pay 40 thousand a year to get raped by a frat boy?")

    show teacher_2:
        xalign 0.86
        linear 2 centerstage
    $ setWait(23.815,26.234)
    $ speak(TEACHER_2, "Ha ha, very funny.")

    show nicole sc4:
        leftstage
        pause 1.6
        xzoom -1
        linear 2.2 off_left

    hide guy_2
    hide girl_4

    $ setWait(26.234,30.364)
    $ speak(NICOLE, "Uh yeah I'm hilarious, get more laughs than you.")

    stop ambient fadeout 2
    jump scene_0095
label scene_0095:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0095.mp3")
    scene gym 3
    play ambient "audio/ambience/gym_ambience.mp3" fadein 1
    show nicole gym:
        centerstage

    show kylar gym unhappy:
        xzoom -1
        rightstage

    show coach 2:
        xzoom -1
        off_left
        linear 0.7 leftstage
    $ setWait(0.731,2.799)
    $ speak(COACH, "Nicole! Get it together!")

    show nicole gym:
        xzoom -1
        linear 1.4 leftcenterstage

    show coach 2:
        leftstage
        pause 1
        xzoom 1
        linear 1.5 off_left
    $ setWait(2.799,6.595)
    $ speak(NICOLE, "The government forces me to be here and you expect me to try at volleyball?")
    show kylar gym angry:
        rightstage
        xzoom 1

    $ setWait(6.595,10.682)
    $ speak(KYLAR, "God dammit our team keeps fucking losing! So fucking gay!")

    show nicole gym:
        xzoom 1

    $ setWait(10.682,11.808)
    $ speak(NICOLE, "What's your problem?")

    show kylar gym furious:
        rightstage
        linear 1 rightcenterstage
    $ setWait(11.808,14.227)
    $ speak(KYLAR, "You fucking whore! Shut up!")
    show nicole gym:
        xzoom -1
        pause 1.8
        xzoom 1
    $ setWait(14.227,18.273)
    $ speak(NICOLE, "Hey coach are we just...? Okay no discipline for that one, go on.")
    $ setWait(18.273,21.818)
    $ speak(KYLAR, "I didn't get into Lacrosse camp, such bullshit!")
    $ setWait(21.818,24.529)
    $ speak(NICOLE, "Well maybe just.. get better at it?")
    $ setWait(24.529,33.029)
    $ speak(KYLAR, "No you don't understand, like there's all these dumb ass under privileged student passes. They're doing so many that like 20 percent of the sports are automatically filled.")
    $ setWait(33.029,38.293)
    $ speak(KYLAR, "All these Mexican kids act like America's so racist when they got the fucking red carpet rolled out for everything.")
    show guy_4 gym:
        off_right
        linear 1.4 rightstage
    $ setWait(38.293,40.962)
    $ speak(GUY_5, "You mean like affirmative action? I think that's what they call it.")
    show kylar gym angry:
        xzoom -1
    $ setWait(40.962,44.049)
    $ speak(KYLAR, "I call it fucking gay. Who's with me?")

    menu:
        "WHO FUCKING CARES":
            jump scene_0096
        "SAY YOU LOVE RAP MUSIC":
            jump scene_0097
label scene_0096:
    $ setVoiceTrack("audio/Scenes/0096.mp3")
    scene gym 3
    show nicole gym:
        leftcenterstage

    show kylar gym angry:
        rightcenterstage
        xzoom -1

    show guy_4 gym:
        rightstage
    $ setWait(0.373,3.001)
    $ speak(NICOLE, "Just shut up and pass the ball, I gotta serve.")
    show kylar gym angry:
        rightcenterstage
        xzoom 1
    $ setWait(3.001,4.92)
    $ speak(KYLAR, "What? How can you side with that?")
    $ setWait(4.92,9.341)
    $ speak(NICOLE, "No one gives a shit but you and men who smoke at chain restaurant bars.")
    $ setWait(9.341,12.886)
    $ speak(KYLAR, "Oh yeah, nothing matters unless you care, I see how it is.")
    $ setWait(12.886,16.056)
    $ speak(NICOLE, "Can you just assume you won the argument so I can stop hearing this?")
    show kylar gym unhappy:
        xzoom -1
    $ setWait(16.056,22.187)
    $ speak(KYLAR, "Fucking women gotta go too, dude. I wanna move to the middle east, a country that stones loud women to death.")
    $ setWait(22.187,24.397)
    $ speak(NICOLE, "Sorry, what country is that?")
    show kylar gym angry:
        xzoom 1
    $ setWait(24.397,29.069)
    $ speak(KYLAR, "I just said, the middle east! For such a smart ass you don't know books too good.")
    stop ambient fadeout 2
    jump scene_0098
label scene_0097:
    $ setVoiceTrack("audio/Scenes/0097.mp3")
    scene gym 3
    show nicole gym:
        leftcenterstage

    show kylar gym angry:
        rightcenterstage
        xzoom -1

    show guy_4 gym:
        rightstage
    $ setWait(0.377,3.755)
    $ speak(NICOLE, "Hey you wanna calm down and just listen to rap music or something?")
    show kylar gym angry:
        rightcenterstage
        xzoom 1
    $ setWait(3.755,9.844)
    $ speak(KYLAR, "Everyone and their fucking rap music now. Whatever happened to classic rock? Or country? Y'know like real music!")
    $ setWait(9.844,12.764)
    $ speak(NICOLE, "Classic rock's classic for a reason, it sucks now.")
    $ setWait(12.764,14.849)
    $ speak(KYLAR, "Oh yeah you probably don't even know where to find it.")
    $ setWait(14.849,18.645)
    $ speak(NICOLE, "Where do you find it? Off graphic tees at failing anchor stores?")
    $ setWait(18.645,24.693)
    $ speak(KYLAR, "No.. Yes.. fuck you. I want rap music off the radio so wigger kids like you can suffer!")
    $ setWait(24.693,26.236)
    $ speak(NICOLE, "How am I a wigger?")
    show kylar gym angry:
        rightcenterstage
        pause 2.8
        xzoom -1
        linear 2.5 off_right
    $ setWait(26.236,30.032)
    $ speak(KYLAR, "Just like.. liking black people or something, whatever!")
    stop ambient fadeout 2
    jump scene_0098
label scene_0098:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0098.mp3")
    play ambient "audio/ambience/office_ambience.mp3" fadein 1.2
    scene office 1
    show nicole sc5:
        leftcenterstage

    show couns 2 smile:
        xalign 0.75
    $ setWait(0.75,4.212)
    $ speak(COUNSELOR, "But that's beside the point, just get your grades up, Nicole.")
    $ setWait(4.212,5.005)
    $ speak(NICOLE, "Uh huh.")
    show couns 2:
        xalign 0.75
    $ setWait(5.005,14.764)
    $ speak(COUNSELOR, "And also if you could stop writing \"death to pedophiles\" on all the whiteboards, that would be great. Promoting violence is so vulgar.")
    $ setWait(14.764,17.35)
    $ speak(NICOLE, "But don't pedophiles deserve to die?")
    $ setWait(17.35,20.729)
    $ speak(COUNSELOR, "Nicole, no one deserves to die.")
    $ setWait(20.729,23.19)
    $ speak(NICOLE, "Wow, that's really peaceful of you.")
    show couns 2 smile:
        xalign 0.75
    $ setWait(23.19,31.615)
    $ speak(COUNSELOR, "I used to be as brash as you at a young age, but then I found a release so satisfying it drained every drop of anger I had.")
    $ setWait(31.615,32.824)
    $ speak(NICOLE, "Was it pedophilia?")
    show couns 2 furious:
        xalign 0.75
    $ setWait(32.824,35.202)
    $ speak(COUNSELOR, "Ugh! How dare you!")
    $ setWait(35.202,36.369)
    $ speak(NICOLE, "You didn't say no.")
    show couns 2:
        xalign 0.75
    $ setWait(36.369,39.789)
    $ speak(COUNSELOR, "That's enough for today, kindly leave.")
    show nicole sc5:
        leftcenterstage
        xzoom -1
        linear 1.8 off_left
    $ setWait(39.789,42.918)
    $ speak(NICOLE, "Finally, god damn.")
    $ setWait(42.918,45.395)
    $ speak(COUNSELOR, "...She almost got me that time.")
    stop ambient fadeout 1.5
    jump scene_0100
label scene_0100:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0100.mp3")
    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 1.2
    scene school int 1
    show girl_5:
        rightstage
    show guy_4 smile:
        xzoom -1
        rightcenterstage
    $ setWait(1.02,2.96)
    $ speak(GUY_5, "Aw cool, you joined to?")
    $ setWait(2.96,9.425)
    $ speak(GIRL_5, "Yeah, it's my heritage I have to support it! But do you think the cross is kinda stretched out on my shirt?")
    $ setWait(9.425,10.551)
    $ speak(GUY_5, "Nah it looks fine.")
    show nicole sc5:
        off_left
        linear 5 leftcenterstage

    show girl_5:
        pause 1
        xzoom -1
        linear 2.5 off_farright

    show guy_4 smile:
        pause 1.8
        linear 2.5 off_right

    $ setWait(10.551,14.93)
    $ speak(GIRL_5, "I don't know, I'll probably see Mr. White to trade it in for a swastika shirt.")
    hide girl_5
    hide guy_4
    $ setWait(14.93,17.141)
    $ speak(NICOLE, "I could've sworn there were less of you last week.")
    show jeffery white happy:
        off_right
        pause 0.6
        linear 2 rightcenterstage
    $ setWait(17.141,18.434)
    $ speak(CRISPIN, "Hey, Nicole!")

    show crispin white:
        off_farright
        linear 1.8 rightstage

    $ setWait(18.434,20.06)
    $ speak(JEFFERY, "Where's your heritage shirt?")
    $ setWait(20.06,21.27)
    $ speak(NICOLE, "My what?")
    $ setWait(21.27,24.44)
    $ speak(JEFFERY, "Y'know, to support this grand cause.")
    $ setWait(24.44,25.858)
    $ speak(NICOLE, "Grand cause...")
    show crispin white unhappy:
        rightstage

    show jeffery white:
        rightcenterstage
    $ setWait(25.858,32.114)
    $ speak(CRISPIN, "Nah Jeffery, you're making it sound weird. What we mean is like, we're just fuckin' down for our heritage y'know?")
    $ setWait(32.114,33.866)
    $ speak(NICOLE, "Why would I care about that?")
    $ setWait(33.866,40.664)
    $ speak(CRISPIN, "When you think about it, everyone's kind of against us as white people y'know? There's nothing more punk rock than being white.")
    show nicole sc5 angry:
        leftcenterstage
    $ setWait(40.664,42.583)
    $ speak(NICOLE, "The only people in punk rock are white.")
    $ setWait(42.583,51.8)
    $ speak(JEFFERY, "Yeah so c'mon, Nicole, you gonna join or what? You're the last girl who hasn't signed up for the White Pride Party. We'd love a pretty girl like you to become one of us.")
    show nicole sc5:
        leftcenterstage
    $ setWait(51.8,55.179)
    $ speak(NICOLE, "Sorry um.. what are the benefits?")
    $ setWait(55.179,57.639)
    $ speak(CRISPIN, "Benefits of what exactly?")
    $ setWait(57.639,60.601)
    $ speak(NICOLE, "Wh-White Nationalism, like what's in it for me?")
    show crispin white:
        rightstage
    $ setWait(60.601,63.187)
    $ speak(CRISPIN, "Well you get these kick ass shirts for one.")
    $ setWait(63.187,69.527)
    $ speak(JEFFERY, "I know what's in it for me. Before everyone just avoided me, like I was a freak or something.")
    $ setWait(69.527,78.744)
    $ speak(JEFFERY, "But then Jecka saw me crying in the hall alone and invited me to the White Pride Party. Now I really belong somewhere, and you can belong too!")
    $ setWait(78.744,84.583)
    $ speak(NICOLE, "So for you it's a club for easy social acceptance?")
    $ setWait(84.583,86.168)
    $ speak(JEFFERY, "Well kinda.")
    $ setWait(86.168,91.507)
    $ speak(NICOLE, "But everybody already hits on me? I'm not desperate for social acceptance.")
    $ setWait(91.507,93.509)
    $ speak(JEFFERY, "I guess there's that.")
    $ setWait(93.509,98.347)
    $ speak(NICOLE, "So let me ask this, now that you're in this club do girls talk to you now?")
    $ setWait(98.347,102.643)
    $ speak(JEFFERY, "Not really.. but the guys, they always talk to me now!")
    $ setWait(102.643,107.189)
    $ speak(NICOLE, "Like for fun, to socialize? Or to give you Pride Party orders?")
    $ setWait(107.189,111.443)
    $ speak(JEFFERY, "Uh... well the orders are fun so kinda both.")
    menu:
        "SEE HOW RACIST HE'D BE\nWITH FEMALE ATTENTION":
            jump scene_0101
        "GET A VIDEO OF THIS MESS":
            jump scene_0104
label scene_0101:
    $ setVoiceTrack("audio/Scenes/0101.mp3")
    scene school int 1
    show nicole sc5 flirt:
        leftcenterstage
    show jeffery white:
        rightcenterstage
    show crispin white:
        rightstage
    $ setWait(0.429,5.426)
    $ speak(NICOLE, "Y'know Jeffery this might be sudden but like, you wanna take me out later?")
    $ setWait(5.426,10.597)
    $ speak(JEFFERY, "Kill you? I couldn't do that, Nicole. Unless of course Mr. White told me to.")
    $ setWait(10.597,14.476)
    $ speak(NICOLE, "No I mean like take me out on a date.")
    show jeffery white blush:
        rightcenterstage
    $ setWait(14.476,20.024)
    $ speak(JEFFERY, "D...Date? You mean like dinner and hugging and kissing?")
    $ setWait(20.024,25.404)
    $ speak(NICOLE, "Yeah all of it, but you're pretty busy with all this white pride stuff, huh?")
    $ setWait(25.404,30.492)
    $ speak(JEFFERY, "Uh well not that busy, I gotta egg a synagogue this Friday but I could make time.")
    show nicole sc5:
        leftcenterstage
    $ setWait(30.492,36.707)
    $ speak(NICOLE, "Aw y'know this Friday's like my only free day for the next like forever so damn, too bad.")
    $ setWait(36.707,39.793)
    $ speak(JEFFERY, "Wh-what? Oh well maybe I don't have to.")
    show jecka white:
        off_left
        xzoom -1
        linear 1.5 leftstage
    show nicole sc5:
        pause 1
        xzoom -1
    show jeffery white:
        rightcenterstage
    $ setWait(39.793,40.794)
    $ speak(JECKA, "Hey guys!")
    $ setWait(40.794,42.129)
    $ speak(CRISPIN, "Oh hey, what's up?")
    $ setWait(42.129,43.756)

    $ speak(NICOLE, "Long time no see.")
    show jecka white:
        leftstage
        linear 1 leftcenterstage

    show nicole sc5:
        leftcenterstage
        pause 0.5
        linear 0.8 leftstage
        xzoom 1
    $ setWait(43.756,49.72)
    $ speak(JECKA, "Jeffery I just wanted to remind you that you need to bring the extra large eggs this Friday, we need a big splat.")
    $ setWait(49.72,53.015)
    $ speak(JEFFERY, "Of course, yeah, about that...")
    show jecka white angry:
        leftcenterstage
    $ setWait(53.015,58.062)
    $ speak(JECKA, "Oh my god I don't wanna hear it, I'm so busy as it is. Seriously if you fuck this up, you're out.")
    show nicole sc5 sad:
        leftstage
        linear 1 xalign 0.08
    $ setWait(58.062,61.148)
    $ speak(NICOLE, "Jeffery, what about our date this Friday?")
    show jecka white angry:
        xzoom 1
        pause 1.3
        xzoom -1
        linear 1 xalign 0.48
    $ setWait(61.148,64.568)
    $ speak(JECKA, "What the fuck is this? I thought you'd die for this cause?")
    $ setWait(64.568,76.33)
    $ speak(JEFFERY, "Sorry Jecka, but I kinda just did this cause no one else would talk to me. But now that Nicole's asking me out, well, having a girlfriend's way more important than the final solution.")
    show crispin white unhappy:
        rightstage
        linear 1 xalign 1.15

    show nicole sc5:
        xalign 0.08
        pause 0.4
        linear 1 xalign -0.14
    $ setWait(76.33,77.581)
    $ speak(CRISPIN, "Dude what?")
    $ setWait(77.581,84.129)
    $ speak(JECKA, "You little fucking race traitor. Mr. White trained me this for moment, Aryan students!")
    show guy_4:
        off_right
        linear 0.8 xalign .8
    $ setWait(84.129,85.631)
    $ speak(GUY_5, "Imperial Scribe Jecka!")
    show girl_5:
        off_right
        linear 0.4 xalign .95
    $ setWait(85.631,87.299)
    $ speak(GIRL_5, "How may we serve you!")
    show jecka white angry:
        xalign 0.48
        linear 2 leftcenterstage
    $ setWait(87.299,93.43)
    $ speak(JECKA, "Jeffery here is no longer our brother and he must be eliminated! Take care of him.")
    $ setWait(93.43,95.307)
    $ speak(GUY_5, "Finally, I thought you'd never ask!")
    show jeffery white:
        rightcenterstage
        pause 2.55
        xzoom -1
        linear 1 xalign 0.55
    $ setWait(95.307,98.852)
    $ speak(GIRL_5, "Yeah I hated being seen with him on rallies.")
    show jecka white:
        leftcenterstage
        xzoom 1
        linear 1 xalign 0.17
    $ setWait(98.852,103.774)
    $ speak(JECKA, "Oh Nicole, we just gotta take care of a little business here but you wanna hang out after school?")
    show nicole sc5 surprised:
        xalign -.14
    $ setWait(103.774,106.151)
    $ speak(NICOLE, "Are you actually just gonna have him killed right here?")
    show jecka white:
        xalign 0.17
        pause 0.8
        xzoom -1

    show guy_4:
        xalign .8
        pause 2.1
        linear 4.5 xalign .55
    show girl_5:
        xalign .95
        pause 2.1
        linear 4.5 xalign .62
    show crispin white:
        xalign 1.15
        pause 2
        linear 4.5 xalign .7
    $ setWait(106.151,109.071)
    $ speak(JECKA, "Well duh but it's just politics, y'know.")
    show black:
        alpha 0.0
        pause 0.8
        linear 1.3 alpha 1.0
    stop ambient fadeout 3
    show jeffery white:
        xalign 0.55
        linear 3 leftcenterstage
    $ setWait(109.071,113.573)
    $ speak(JEFFERY, "Help me!")
    jump scene_0102
label scene_0102:
    $ setVoiceTrack("audio/Scenes/0102.mp3")
    play ambient "audio/ambience/exterior_ambience.mp3" fadein 3
    scene onlayer master
    show black
    show diner ext with Pause(4.802):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 4.802 zoom .6 truecenter
    scene diner int
    play ambient "audio/ambience/diner_ambience.mp3"
    show nicole sc5:
        leftcenterstage
    show jecka white unhappy:
        rightcenterstage
    $ setWait(4.802,8.681)
    $ speak(NICOLE, "So how's Mr. White doing?")
    $ setWait(8.681,17.44)
    $ speak(JECKA, "Well he gave medals to everyone who killed Jeffery so I'd take it he's pretty happy. But can I vent like, they're not even medals just little shirt pins.")
    $ setWait(17.44,24.947)
    $ speak(NICOLE, "Yeah fatal excommunication's definitely one of the less gratifying felonies. At least when you rob a bank you get money.")
    $ setWait(24.947,28.367)
    $ speak(JECKA, "Speaking of Mr. White, he's like obsessed with you.")
    $ setWait(28.367,29.326)
    $ speak(NICOLE, "Still?")
    $ setWait(29.326,32.288)
    $ speak(JECKA, "Always asks about you, always talks about you.")
    $ setWait(32.288,34.039)
    $ speak(NICOLE, "What was the last thing he asked?")
    $ setWait(34.039,37.042)
    $ speak(JECKA, "He asked if Montana sounded like a good name for a death camp.")
    $ setWait(37.042,38.502)
    $ speak(NICOLE, "No-- about me.")
    $ setWait(38.502,47.261)
    $ speak(JECKA, "Always about you-- Okay. Well he wasn't really asking, just wondering aloud if your hair was too dark for you to bear racially pure children.")
    $ setWait(47.261,48.429)
    $ speak(NICOLE, "...What the fuck.")
    stop ambient fadeout 9
    show jecka white unhappy:
        rightcenterstage
        pause 5.2
        linear 0.8 xalign .59
    show black:
        alpha 0
        pause 7.2
        linear 3.3 alpha 1.0
    $ setWait(48.429,61.144)
    $ speak(JECKA, "I know, it's so obvious you dye it, right? ...Right?")
    jump end_0103

label end_0103:
    show black onlayer screens with Pause(1.3):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0103" not in persistent.endings:
        $ persistent.endings.append("end_0103")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0103end with Pause (42.7):
        alpha 1.0
    return

label scene_0104:
    $ setVoiceTrack("audio/Scenes/0104.mp3")
    scene school int 1
    show nicole sc5:
        leftcenterstage
    show jeffery white:
        rightcenterstage
    show crispin white:
        rightstage
    $ setWait(0.334,4.505)
    $ speak(NICOLE, "So what are the orders? Do you guys do a bunch of chants or something?")
    $ setWait(4.505,5.548)
    $ speak(CRISPIN, "For sure, dude.")
    $ setWait(5.548,8.05)
    $ speak(JEFFERY, "Yeah we could show you some if you'd like!")
    $ setWait(8.05,14.598)
    $ speak(NICOLE, "Well I was wondering if I could maybe.. take a video of it? Just so I could review at home and practice.")
    $ setWait(14.598,16.267)
    $ speak(JEFFERY, "Oh so you're joining?")
    show nicole sc5:
        leftcenterstage
        pause 1
        linear 1.8 leftstage
    $ setWait(16.267,19.145)
    $ speak(NICOLE, "I didn't say that but maybe this could convince me.")

    show jeffery white happy:
        rightcenterstage
        linear 1.1 xalign .46
    show crispin white:
        rightstage
        pause 3.1
        linear 1 xalign .7
    $ setWait(19.145,23.107)
    $ speak(JEFFERY, "Alright, you better start rolling! Aryan brothers, assemble!")
    show guy_4 smile:
        off_right
        linear 1.3 rightstage
    $ setWait(23.107,24.317)
    $ speak(GUY_5, "Yo, we doing the chant?")
    show crispin white:
        xzoom -1
    $ setWait(24.317,25.901)
    $ speak(CRISPIN, "Hell yeah we're doing the chant!")
    show crispin white:
        xalign .7
        xzoom 1
    $ setWait(25.901,28.529)
    $ speak(WPP, "White! Pride! Worldwide!")
    show nicole sc5 sly:
        leftstage
    $ setWait(28.529,32.199)
    $ speak(NICOLE, "Yeah awesome, you're doing great, guys.")
    show jeffery white:
        xalign .46
        linear 1.5 leftcenterstage
    $ setWait(32.199,34.702)
    $ speak(JEFFERY, "So how 'bout it, Nicole? You gonna join?")
    $ setWait(34.702,42.293)
    $ speak(NICOLE, "I don't know, you really made a convincing argument with this.\nCan I take this video home and watch it a few times?")
    $ setWait(42.293,46.255)
    $ speak(JEFFERY, "Sure, I can come over and do more chants too if you'd like.")

    show nicole sc5:
        leftstage
    show black:
        alpha 0.0
        pause 2
        linear 2 alpha 1.0

    stop ambient fadeout 4.2
    $ setWait(46.255,50.966)
    $ speak(NICOLE, "Uh, nah that's okay.")
    jump scene_0104b
label scene_0104b:
    $ setVoiceTrack("audio/Scenes/0104b.mp3")
    play ambient "audio/Ambience/Neighborhood_Ambience_Night.mp3" fadein 2
    scene onlayer master
    show black
    show home nicole ext night with Pause(2.466):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.466 zoom .6 truecenter
    scene bedroom nicole
    show nicole sc5 sly:
        xzoom -1
        rightcenterstage
    play ambient "audio/Ambience/House_Night_Ambience.mp3"
    $ setWait(2.466,9.272)
    $ speak(NICOLE, "Okay, let's see what the Nation of Islam forums have to say about this.. Upload!")
    stop ambient fadeout 2
    jump end_0105

label end_0105:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0105" not in persistent.endings:
        $ persistent.endings.append("end_0105")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0105end with Pause (28.7):
        alpha 1.0
    return

label scene_0106:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 2.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0106.mp3")
    scene cafeteria int 2
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1.4
    show nicole sc3:
        rightcenterstage

    show jecka sc3 unhappy:
        rightstage

    $ setWait(0.1,1.876)
    $ speak(JECKA, "")
    $ setWait(1.876,2.836)
    $ speak(JECKA, "...Him?")
    $ setWait(2.836,6.006)
    $ speak(NICOLE, "Yeah what's wr-- I'm just kidding I know what's wrong with him.")
    $ setWait(6.006,11.97)
    $ speak(JECKA, "But like, you went over to his house. He's a total jock, you know what jocks do.")
    $ setWait(11.97,13.555)
    $ speak(NICOLE, "...Get molested by their coach?")
    show jecka sc3 angry:
        rightstage
    $ setWait(13.555,19.144)
    $ speak(JECKA, "Yeah! And then they take it out on you. When he got you a drink did you watch him pour it?")
    $ setWait(19.144,21.146)
    $ speak(NICOLE, "He never got me a drink.")
    $ setWait(21.146,23.898)
    $ speak(JECKA, "Wha-- No drink? Did he offer a drink?")
    $ setWait(23.898,25.442)
    $ speak(NICOLE, "Did not offer a drink.")
    $ setWait(25.442,28.445)
    $ speak(JECKA, "What a fucking asshole, see they're all like this too.")
    $ setWait(28.445,30.071)
    $ speak(NICOLE, "At least I didn't get drugged.")
    $ setWait(30.071,33.074)
    $ speak(JECKA, "I'd rather get drugged than not offered a drink!")
    show nicole sc3 smile:
        rightcenterstage
    $ setWait(33.074,37.328)
    $ speak(NICOLE, "..Y'know what's fun about us is our priorities are drastically different.")
    show jecka sc3 unhappy:
        rightstage
    $ setWait(37.328,39.039)
    $ speak(JECKA, "So anything else from last night?")
    show nicole sc3:
        rightcenterstage
    $ setWait(39.039,42.292)
    $ speak(NICOLE, "Yeah he really wants me to be his girlfriend but y'know.")
    $ setWait(42.292,46.254)
    $ speak(JECKA, "He has the temper problem, right? How'd you turn him down gently?")
    $ setWait(46.254,53.678)
    $ speak(NICOLE, "I didn't turn him down, I.. challenged him to win me over, under the assumption there's some chance I could like him.")
    $ setWait(53.678,55.346)
    $ speak(JECKA, "But in reality there's no chance?")
    $ setWait(55.346,56.306)
    $ speak(NICOLE, "None.")
    show jecka sc3:
        rightstage
    $ setWait(56.306,60.977)
    $ speak(JECKA, "Well good luck with that. Do you want my number in case he revenge-kidnaps you?")
    $ setWait(60.977,63.046)
    $ speak(NICOLE, "I think I already have your number.")
    stop ambient fadeout 2
    jump scene_0107
label scene_0107:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0107.mp3")
    play ambient "audio/Ambience/Classroom_Ambience.mp3" fadein 1.7
    scene classroom int 2
    show couns 2:
        rightstage

    show nicole sc3:
        leftstage

    show girl_1 color2:
        xalign .28


    show jecka sc3 unhappy:
        xzoom -1
        xalign .55
    $ setWait(0.02,0.713)
    $ speak(COUNSELOR, "")
    $ setWait(0.713,10.097)
    $ speak(COUNSELOR, "But yes the rumors were true, your beloved gym teacher, Coach Colby, was having illicit relationships with some of your classmates.")
    $ setWait(10.097,11.14)
    $ speak(KYLAR, "Rock on, Coach!")
    show couns 2:
        xzoom -1
        pause 2
        xzoom 1
    $ setWait(11.14,27.031)
    $ speak(COUNSELOR, "Kylar. Anyway, his position of gym teacher has been terminated and will be replaced by next week. If any students had unfortunate run-ins with this behavior, my office is always open to talk about it.")
    $ setWait(27.031,31.785)
    $ speak(GIRL_1, "Yeah I was in his class and he always wanted to try and guess what kind of underwear we had on.")
    show jecka sc3:
        xzoom 1
    $ setWait(31.785,33.412)
    $ speak(JECKA, "Oh I remember that.")
    $ setWait(33.412,37.249)
    $ speak(COUNSELOR, "I'm so sorry you had to go through that, both of you.")
    $ setWait(37.249,39.919)
    $ speak(GIRL_1, "Well no the fucked up part was he always guessed it right.")
    show jecka sc3 unhappy:
        xzoom -1
    $ setWait(39.919,41.67)
    $ speak(JECKA, "It's like he was psychic.")
    $ setWait(41.67,43.214)
    $ speak(NICOLE, "Or spying on you.")
    $ setWait(43.214,54.058)
    $ speak(COUNSELOR, "Now Nicole, just because he made a mistake or two doesn't mean he would actively spy on the girl's locker room. Why do you feel the need to be pessimistic?")
    menu:
        "LIE FOR A PITY PARTY":
            jump scene_0108
        "FLIRT WITH HIM AS A JOKE":
            jump scene_0109
label scene_0108:
    $ setVoiceTrack("audio/Scenes/0108.mp3")
    scene classroom int 2
    show couns 2:
        rightstage

    show nicole sc3:
        leftstage

    show girl_1 color2:
        xalign .28

    show jecka sc3 unhappy:
        xzoom -1
        xalign .55
    $ setWait(0.134,2.67)
    $ speak(NICOLE, "Uh, cause I'm a victim of that psycho?")
    $ setWait(2.67,3.713)
    $ speak(GIRL_1, "You too?")
    $ setWait(3.713,8.467)
    $ speak(NICOLE, "Uh-- Yeah he like locked me in his office and did things.")
    $ setWait(8.467,9.302)
    $ speak(KYLAR, "Like what?")
    show couns 2:
        xzoom -1
    $ setWait(9.302,15.85)
    $ speak(COUNSELOR, "Now Kylar, you should know it's disrespectful of your classmate to ask the details of her sexual assault.")
    show jecka sc3 unhappy:
        xzoom 1

    $ setWait(15.85,17.56)
    $ speak(JECKA, "I mean I kinda wanna hear.")
    show couns 2:
        xzoom 1

    show jecka sc3 unhappy:
        xalign .55
        pause 5
        linear 4 off_left

    show girl_1 color2:
        xalign .28
        pause 5
        linear 3.6 off_farleft

    show nicole sc3:
        leftstage
        pause 5.3
        linear 2.1 rightcenterstage


    $ setWait(17.56,25.192)
    $ speak(COUNSELOR, "Class dismissed! Everyone out but Nicole, I'd like to have a word with you.")

    show nicole sc3:
        rightcenterstage
    $ setWait(25.192,29.196)
    $ speak(NICOLE, "Can we fast forward this to the part where you tell me I'm not alone so I can leave?")
    show couns 2 smile:
        rightstage
    $ setWait(29.196,35.036)
    $ speak(COUNSELOR, "Well I wouldn't give any old lecture to you, Nicole. One of our brightest students deserves better.")
    $ setWait(35.036,36.912)
    $ speak(NICOLE, "I have a C+ average.")
    $ setWait(36.912,45.129)
    $ speak(COUNSELOR, "Not to mention beautiful. I just love to see you whimsically stroll up and down the hallways between classes.")
    show nicole sc3 surprised:
        rightcenterstage
    $ setWait(45.129,46.547)
    $ speak(NICOLE, "Is this happening right now?")
    $ setWait(46.547,54.68)
    $ speak(COUNSELOR, "Nicole, how would you feel about participating in some.. extracurricular learning exercises?")
    show nicole sc3:
        rightcenterstage
    $ setWait(54.68,57.558)
    $ speak(NICOLE, "Will I learn how to exercise my right to say \"no\"?")
    $ setWait(57.558,66.859)
    $ speak(COUNSELOR, "Now now, be serious. My car's nearby in the staff parking lot. I have the key fob which starts the air conditioning remotely.")
    $ setWait(66.859,68.819)
    $ speak(NICOLE, "Oh well now you're winning me over.")
    $ setWait(68.819,79.33)
    $ speak(COUNSELOR, "How bout it? I could help you with your homework using the faculty answer keys. And I can tell you have many ways of repaying me just by looking at you.")
    menu:
        "SCREAM AND GET ANOTHER ONE FIRED":
            jump scene_0110
        "USE HIM TO SKIP SCHOOL":
            jump scene_0111
label scene_0109:
    $ setVoiceTrack("audio/Scenes/0109.mp3")
    scene classroom int 2
    show couns 2:
        rightstage

    show nicole sc3 flirt:
        leftstage

    show girl_1 color2:
        xalign .28


    show jecka sc3 unhappy:
        xzoom -1
        xalign .55
    $ setWait(0.423,8.056)
    $ speak(NICOLE, "Sorry sir. I guess I get flustered around dominant male authority figures.")

    show jecka sc3 unhappy:
        pause 3.7
        xzoom 1
        linear 3.6 off_left

    show girl_1 color2:
        pause 3.5
        linear 3.2 off_farleft

    show kylar sc3:
        off_right
        pause 3
        linear 5.3 off_left

    show nicole sc3:
        pause 5.5
        linear 2 rightcenterstage
        pause 0.2
        xzoom -1

    $ setWait(8.056,14.02)
    $ speak(COUNSELOR, "Oh um-- well that's no excuse! Class dismissed, except for you, Nicole.")
    $ setWait(14.02,15.605)
    $ speak(KYLAR, "Ha bitch sucks to be you.")
    $ setWait(15.605,20.568)
    $ speak(NICOLE, "Sucks to like lacrosse you fucking field hockey reject.")
    hide kylar sc3
    hide jecka sc3
    hide girl_1
    show nicole sc3:
        rightcenterstage
        pause 0.4
        xzoom 1

    show couns 2 smile:
        rightstage
    $ setWait(20.568,25.156)
    $ speak(COUNSELOR, "Now that your classmates are gone.. you wanna get out of here with me?")
    $ setWait(25.156,26.366)
    $ speak(NICOLE, "I'm sorry, what?")
    $ setWait(26.366,41.214)
    $ speak(COUNSELOR, "Don't play naive, Nicole. I saw the way you looked at me. I've seen the way you've been looking at me since you got to this school. Your dominant male authority figure's here to take you away.")
    show nicole sc3 surprised:
        rightcenterstage
    $ setWait(41.214,44.717)
    $ speak(NICOLE, "Oh.. so you're like actually going for it.")
    $ setWait(44.717,52.267)
    $ speak(COUNSELOR, "As the counselor I could sign you out early. We could spend the rest of the afternoon together, the evening too?")
    menu:
        "SCREAM AND GET ANOTHER ONE FIRED":
            jump scene_0110
        "USE HIM TO SKIP SCHOOL":
            jump scene_0111
label scene_0110:
    $ setVoiceTrack("audio/Scenes/0110.mp3")
    scene classroom int 2
    show nicole sc3 scream:
        xzoom -1
        rightcenterstage
    show couns 2:
        rightstage
    $ setWait(0.134,4.006)
    $ speak(NICOLE, "Help! You got another guy trying to date minors in here!")
    $ setWait(4.006,6.175)
    $ speak(COUNSELOR, "Okay calm down! Forget I said anything!")
    show nicole sc3:
        xzoom 1
        rightcenterstage
        pause 3.8
        xzoom -1
    $ setWait(6.175,12.097)
    $ speak(NICOLE, "Dude you can't get rejected and then pretend you didn't ask me out. Quick! Principal Lynn! Anyone!")
    show lynn:
        xzoom -1
        off_left
        linear 0.45 leftstage
    $ setWait(12.097,15.559)
    $ speak(LYNN, "What is going on in here? Nicole, why are you screaming?")
    $ setWait(15.559,17.895)
    $ speak(NICOLE, "He literally just invited me over to fuck.")
    show lynn:
        leftstage
        linear 0.7 leftcenterstage
    $ setWait(17.895,19.897)
    $ speak(LYNN, "Excuse me? Is this true?")
    show couns 2:
        xzoom -1
        pause 0.9
        xzoom 1
    $ setWait(19.897,22.941)
    $ speak(COUNSELOR, "Uh-- well I didn't use the F-word!")
    show lynn:
        pause 1.8
        xzoom 1
    $ setWait(22.941,25.778)
    $ speak(LYNN, "It's like every week now. Security!")
    show cop:
        xzoom -1
        off_left
        linear 0.4 leftstage
    $ setWait(25.778,26.695)
    $ speak(COP, "Yes Principal!")
    show lynn:
        xzoom -1
    $ setWait(26.695,29.239)
    $ speak(LYNN, "Arrest this man for criminal misconduct.")
    show nicole sc3 sly:

        rightcenterstage
        linear 1.6 leftcenterstage
        xzoom 1

    show lynn:
        leftcenterstage
        linear 1.3 leftstage

    show cop:
        leftstage
        linear 1.8 rightcenterstage
        pause 0.4
        linear 0.1 xalign .85
    $ setWait(29.239,31.575)
    $ speak(COUNSELOR, "Now let's remain reasonable here.")
    show couns 2:
        xzoom -1
        rightstage
        linear 4 xalign 0.9

    show cop:
        xzoom -1
        xalign .85
        linear 4 xalign .75
    $ setWait(31.575,35.871)
    $ speak(COP, "You have the right to remain silent, anything you say can and will be used--")
    show couns 2 furious:
        xzoom -1
        xalign 0.9
    $ setWait(35.871,39.958)
    $ speak(COUNSELOR, "Fuck! No! This is all your fault you fucking whore!")
    $ setWait(39.958,46.006)
    $ speak(NICOLE, "Wow that was mean. He also threatened to kill me if I didn't have sex with him so throw that somewhere in the charges.")
    $ setWait(46.006,47.216)
    $ speak(COP, "Come with me!")
    show couns 2 furious:
        xalign 0.9
        linear 4.25 off_left

    show cop:
        xalign .75
        linear 4 xalign -0.5

    show nicole sc3 sly:
        leftcenterstage
        pause 1
        linear 1.1 xalign 0.64
        xzoom -1

    show lynn:
        leftstage
        pause 1.3
        linear 1.2 xalign .38
        xzoom 1
    $ setWait(47.216,50.11)
    $ speak(COUNSELOR, "No don't! Don't listen to her!")
    stop ambient fadeout 1.5
    jump scene_0112
label scene_0111:
    $ setVoiceTrack("audio/Scenes/0111.mp3")
    scene classroom int 2
    show nicole sc3:
        rightcenterstage
    show couns 2 smile:
        rightstage
    $ setWait(0.464,2.874)
    $ speak(NICOLE, "You know I'm 16, right?")
    $ setWait(2.874,5.21)
    $ speak(COUNSELOR, "Age is just a number.")
    $ setWait(5.21,11.007)
    $ speak(NICOLE, "Hm... Well I guess saying that makes you just a pedophile so what's the worst that could happen?")
    $ setWait(11.007,16.054)
    $ speak(COUNSELOR, "See, there's that open-mindedness our program really tries to promote.")
    show nicole sc3 sly:
        rightcenterstage
    $ setWait(16.054,22.31)
    $ speak(NICOLE, "Yeah, and believe me, your mind's gotta be wide open to date your guidance counselor. Like your brain won't even fit.")
    show couns 2 smile:
        pause 2.7
        linear 5 off_left
    show nicole sc3:
        pause 4.9
        xzoom -1
    $ setWait(22.31,27.364)
    $ speak(COUNSELOR, "Heh such a funny girl, come with me.")
    stop ambient fadeout 2
    jump scene_0113
label scene_0112:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0112.mp3")
    scene school ext 4
    play ambient "audio/ambience/school_ext_ambience.mp3" fadein 1.4
    show cop:
        xzoom -1
        leftstage
    show couns 2 furious:
        xzoom -1
        xalign 0.17

    $ setWait(0.882,2.091)
    $ speak(COP, "Bring the car around front!")
    show girl_3:
        off_right
        linear 2 xalign 0.48
    $ setWait(2.091,4.886)
    $ speak(GIRL_3, "What's happening!? Why's the counselor in handcuffs!")
    $ setWait(4.886,7.055)
    $ speak(COUNSELOR, "What the fuck is everyone out here for!?")
    show lynn:
        off_right
        linear 2 xalign .71
    $ setWait(7.055,12.894)
    $ speak(LYNN, "Today was the school bake sale. Apparently you picked the worst day to ask a student out.")
    $ setWait(12.894,15.021)
    $ speak(GIRL_3, "Oh my god another pedophile!")
    show nicole sc3:
        xzoom -1
        off_right
        linear 1 rightstage
    $ setWait(15.021,16.272)
    $ speak(NICOLE, "Tell me about it.")
    $ setWait(16.272,18.107)
    $ speak(KYLAR, "Hey! Nicole!")
    show girl_3 shock:
        xzoom -1

    show lynn:
        xzoom 1
        pause 0.9
        xzoom -1

    show nicole sc3:
        rightstage
        xzoom -1
        pause 1.1
        xzoom 1
    $ setWait(18.107,19.859)
    $ speak(GIRL_3, "Look, on the roof!")
    show suicide
    $ setWait(19.859,23.154)
    $ speak(KYLAR, "Impressed now!?")
    $ setWait(23.154,25.073)
    $ speak(LYNN, "Kylar, get down from there!")
    $ setWait(25.073,29.869)
    $ speak(KYLAR, "Oh I will, I'm gonna jump! For you Nicole!")
    hide suicide
    $ setWait(29.869,31.829)
    $ speak(NICOLE, "Are you serious right now?")
    show suicide
    hide cop
    hide couns

    $ setWait(31.829,37.293)
    $ speak(KYLAR, "You said you wanted someone not boring, so I'm gonna stick the ultimate landing!")

    show nicole sc3:
        xzoom -1
        rightstage
    show lynn:
        xzoom -1
        rightcenterstage

    show girl_3 shock:
        leftstage
        xzoom -1

    hide suicide
    $ setWait(37.293,38.962)
    $ speak(LYNN, "You told him to do this?")
    $ setWait(38.962,42.966)
    $ speak(NICOLE, "Well first I told him to fuck off but he wouldn't take no for an answer.")
    show suicide
    $ setWait(42.966,48.012)
    $ speak(LYNN, "One girl isn't worth the rest of your life, don't kill yourself!")
    hide girl_3
    $ setWait(48.012,53.059)
    $ speak(KYLAR, "I'm not! If I stick the landing I won't be hurt at all! Saw it on MySpace!")
    hide suicide
    $ setWait(53.059,54.894)
    $ speak(LYNN, "Oh my god, stop him, Nicole!")
    $ setWait(54.894,56.646)
    $ speak(NICOLE, "Why!? He's got it figured out.")
    $ setWait(56.646,62.694)
    $ speak(LYNN, "I can't have 2 pedophile arrests and a student attempting suicide in one week! Really need to keep this job.")
    show nicole sc3:
        xzoom -1
        rightstage
        pause 1.35
        xzoom 1

    show suicide:
        alpha 0.0
        pause 2.6
        alpha 1.0
    $ setWait(62.694,66.447)
    $ speak(NICOLE, "Fine uh.. Kylar!")
    $ setWait(66.447,67.991)
    $ speak(KYLAR, "What?")
    menu:
        "DON'T CARE":
            jump scene_0114
        "PRETEND TO CARE SO HE DEFINITELY JUMPS":
            jump scene_0115
label scene_0113:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0113.mp3")
    scene school ext 4
    play ambient "audio/ambience/school_ext_ambience.mp3" fadein 1.4
    show couns 2:
        off_right
        linear 3 leftcenterstage
    $ setWait(1.755,2.756)
    $ speak(COUNSELOR, "This way, Nicole!")
    show girl_3 smile:
        xzoom -1
        off_left
        linear 0.65 leftstage
    show nicole sc3:
        xzoom -1
        off_right
        pause 2.5
        linear 3 rightcenterstage
    $ setWait(2.756,7.719)
    $ speak(GIRL_3, "Hey it's our Counselor! Could we interest you in some homemade cake? 5 dollars!")
    $ setWait(7.719,8.887)
    $ speak(COUNSELOR, "What is this?")
    show girl_3:
        leftstage
    $ setWait(8.887,11.181)
    $ speak(GIRL_3, "Ugh fine okay 4 dollars.")
    show couns 2:
        xzoom -1
    $ setWait(11.181,13.058)
    $ speak(COUNSELOR, "Why is everyone out here?")
    $ setWait(13.058,15.977)
    $ speak(NICOLE, "You work here and didn't know the school bake sale's today?")
    $ setWait(15.977,18.647)
    $ speak(COUNSELOR, "So you knew and let us go this way anyway?")
    show couns 2:
        pause 1
        xzoom 1
    $ setWait(18.647,22.275)
    $ speak(GIRL_3, "Were you guys just leaving together? Did the new girl get suspended or something?")
    $ setWait(22.275,24.235)
    $ speak(NICOLE, "No actually he was taking me out on a date--")
    $ setWait(24.235,26.029)
    $ speak(KYLAR, "Nicole! Up here!")
    show girl_3 shock:
        xzoom -1
        leftstage
    $ setWait(26.029,28.073)
    $ speak(GIRL_3, "How'd he get on the roof!?")
    show nicole sc3:
        xzoom 1
    show couns 2:
        xzoom -1
    $ setWait(28.073,28.698)
    $ speak(NICOLE, "What?")
    show suicide b:
        alpha 0.0
        pause 2.6
        alpha 1.0
    $ setWait(28.698,34.162)
    $ speak(KYLAR, "You wanted not boring? Well you got it! I'm gonna jump!")
    hide suicide b
    show lynn:
        off_right
        linear 0.8 rightstage
        xzoom -1
    $ setWait(34.162,37.123)
    $ speak(LYNN, "What is this-- Kylar! Get down from there now!")
    show suicide
    $ setWait(37.123,42.796)
    $ speak(KYLAR, "No problem, I'm gonna stick the greatest landing of all time for you, Nicole.")
    hide suicide
    show nicole sc3 surprised:
        rightcenterstage
    $ setWait(42.796,44.089)
    $ speak(NICOLE, "Am I awake right now?")
    show suicide
    $ setWait(44.089,50.053)
    $ speak(KYLAR, "Don't worry, Miss Lynn. MySpace showed me how to land risky jumps without injury! I'm coming down!")
    hide suicide
    show lynn:
        rightstage
        pause 2.43
        xzoom 1

    show nicole sc3:
        rightcenterstage
    $ setWait(50.053,54.724)
    $ speak(LYNN, "No, stay there! Do something, Nicole. You're the only one he'll listen to.")
    $ setWait(54.724,57.686)
    $ speak(NICOLE, "Isn't this your job? I don't care if he gets himself killed.")
    $ setWait(57.686,60.23)
    $ speak(LYNN, "Now's not the time, just keep him talking!")
    show suicide:
        alpha 0.0
        pause 1.7
        alpha 1.0
    $ setWait(60.23,63.358)
    $ speak(NICOLE, "Fine.. uh, Kylar!")
    $ setWait(63.358,66.569)
    $ speak(KYLAR, "What is it? Last thing before I jump!")
    menu:
        "DON'T CARE":
            jump scene_0114
        "PRETEND TO CARE SO HE DEFINITELY JUMPS":
            jump scene_0115
label scene_0114:
    $ setVoiceTrack("audio/Scenes/0114.mp3")
    scene school ext 4
    show nicole sc3:
        rightstage
        xzoom 1
    show lynn:
        rightcenterstage
        xzoom -1
    $ setWait(0.584,6.339)
    $ speak(NICOLE, "Hey I gotta be honest, I don't really give a shit if you stick some awesome landing!")
    show suicide
    $ setWait(6.339,8.341)
    $ speak(KYLAR, "What, Really?")
    hide suicide
    $ setWait(8.341,9.426)
    $ speak(NICOLE, "Yeah really cause like--")
    show suicide
    $ setWait(9.426,15.265)
    $ speak(KYLAR, "Cause you love me for me! You don't need some wild display of courage to be my girlfriend!")
    $ setWait(15.265,22.689)
    $ speak(NICOLE, "No actually I'm just not gonna be your girlfriend either way, you had zero chance from the start if it makes you feel any better.")
    $ setWait(22.689,24.232)
    $ speak(KYLAR, "What!? No!")
    show suicide:
        alpha 0.0
        pause 1
        alpha 1.0
    show nicole sc3:
        rightstage
        xzoom 1
    $ setWait(24.232,31.49)
    $ speak(LYNN, "Why did you say that-- No, Kylar it's okay! Just take some deep breaths, back off from the ledge!")
    jump scene_0116
label scene_0115:
    $ setVoiceTrack("audio/Scenes/0115.mp3")
    scene school ext 4
    show nicole sc3 smile:
        rightstage
        xzoom 1
    show lynn:
        rightcenterstage
        xzoom -1
    show suicide:
        alpha 0.0
        pause 1.6
        alpha 1.0
    $ setWait(0.629,6.385)
    $ speak(NICOLE, "If you jump... I'll be your girlfriend for sure! I never thought you were serious about this!")
    $ setWait(6.385,9.555)
    $ speak(KYLAR, "I am! I love you more than lacrosse!")
    $ setWait(9.555,15.311)
    $ speak(NICOLE, "And if we're still together in 2 years, I'll marry you after graduation!")
    hide suicide
    show nicole sc3:
        xalign 0.85

    show lynn:
        xzoom -1
        xalign 0.6

    $ setWait(15.311,16.604)
    $ speak(LYNN, "What the fuck are you doing?")
    $ setWait(16.604,19.064)
    $ speak(KYLAR, "Aw sick! Here goes nothing!")
    show girl_3 shock:
        off_left
        xzoom -1
        linear 0.7 leftstage
    $ setWait(19.064,20.441)
    $ speak(GIRL_3, "He really jumped!")
    show nicole sc3 surprised:
        xalign 0.85
        linear 0.9 centerstage
    show lynn:
        xalign 0.6
        pause 0.15
        linear 0.8 xalign 0.25

    show kylar fall:
        xalign 1.3 yalign -10.3
        pause 0.65
        linear 0.17 yalign 9.2

    show white onlayer screens:
        xalign 0.5
        alpha 0.0
        pause 0.9
        alpha 1.0
        pause 0.04
        alpha 0.0
        pause 0.04
        alpha 1.0
        pause 0.04
        alpha 0.0
        pause 0.04
        alpha 1.0
        pause 0.04
        alpha 0.0

    show z1zdust:
        alpha 0.0
        pause 0.87
        alpha 1.0
        pause 0.05
        alpha 0.0

    show z2zdust:
        alpha 0.0
        pause 0.92
        alpha 1.0
        pause 0.041
        alpha 0.0

    show z3zdust:
        alpha 0.0
        pause .961
        alpha 1.0
        pause 0.041
        alpha 0.0

    show z4zdust:
        alpha 0.0
        pause 1.002
        alpha 1.0
        pause 0.082
        alpha 0.0

    show z5zdust:
        alpha 0.0
        pause 1.084
        alpha 1.0
        pause 0.082
        alpha 0.0

    show z6zdust:
        alpha 0.0
        pause 1.166
        alpha 1.0
        pause 0.082
        alpha 0.0

    show z7zdust:
        alpha 0.0
        pause 1.284
        alpha 1.0
        pause 0.082
        alpha 0.0

    show z8zdust:
        alpha 0.0
        pause 1.366
        alpha 1.0
        pause 0.082
        alpha 0.0


    $ setWait(20.441,23.486)
    $ speak(KYLAR, "Ahhhhh!!!")
    show nicole sc3 sly:
        centerstage
    $ setWait(23.486,24.32)
    $ speak(NICOLE, "Ow.")
    show lynn:
        xalign 0.25
        linear 1.2 off_right
    $ setWait(24.32,26.113)
    $ speak(LYNN, "Oh my god!")
    stop ambient fadeout 2
    jump scene_0117
label scene_0116:
    $ setVoiceTrack("audio/Scenes/0116.mp3")
    scene school ext 4
    show suicide:
        alpha 1.0
        pause 2.6
        alpha 0.0

    show nicole sc3:
        rightstage
        xzoom 1
        alpha 0.0
        pause 2.6
        alpha 1.0

    show lynn:
        rightcenterstage
        xzoom -1
        alpha 0.0
        pause 2.6
        alpha 1.0

    $ setWait(0.334,4.213)
    $ speak(KYLAR, "All I deserve is a deep plunge! You did this, Nicole!")
    hide suicide
    show nicole sc3:
        rightstage
    show lynn:
        rightcenterstage
        xzoom 1
        linear 1.1 off_left
    $ setWait(4.213,5.13)
    $ speak(LYNN, "Oh god.")
    show nicole sc3:
        rightstage
        linear 0.9 centerstage

    show kylar fall:
        xalign 1.3 yalign -10.3
        pause 0.65
        linear 0.17 yalign 9.2

    show white onlayer screens:
        xalign 0.5
        alpha 0.0
        pause 0.9
        alpha 1.0
        pause 0.04
        alpha 0.0
        pause 0.04
        alpha 1.0
        pause 0.04
        alpha 0.0
        pause 0.04
        alpha 1.0
        pause 0.04
        alpha 0.0

    show z1zdust:
        alpha 0.0
        pause 0.87
        alpha 1.0
        pause 0.05
        alpha 0.0

    show z2zdust:
        alpha 0.0
        pause 0.92
        alpha 1.0
        pause 0.041
        alpha 0.0

    show z3zdust:
        alpha 0.0
        pause .961
        alpha 1.0
        pause 0.041
        alpha 0.0

    show z4zdust:
        alpha 0.0
        pause 1.002
        alpha 1.0
        pause 0.082
        alpha 0.0

    show z5zdust:
        alpha 0.0
        pause 1.084
        alpha 1.0
        pause 0.082
        alpha 0.0

    show z6zdust:
        alpha 0.0
        pause 1.166
        alpha 1.0
        pause 0.082
        alpha 0.0

    show z7zdust:
        alpha 0.0
        pause 1.284
        alpha 1.0
        pause 0.082
        alpha 0.0

    show z8zdust:
        alpha 0.0
        pause 1.366
        alpha 1.0
        pause 0.082
        alpha 0.0

    show girl_3:
        off_left
        xzoom -1
        linear 1 leftstage

    $ setWait(5.13,8.175)
    $ speak(KYLAR, "Aaahhhh!!!")
    hide lynn
    show nicole sc3 sly:
        centerstage
    $ setWait(8.175,11.762)
    $ speak(NICOLE, "What was that 90's TV show, did I do that?")
    show girl_3 smile:
        leftstage
        linear 1 leftcenterstage
    $ setWait(11.762,14.932)
    $ speak(GIRL_3, "I'm traumatized right now but that was actually pretty good.")
    show couns 2:
        off_left
        xzoom -1
        linear 0.8 xalign -.12
    $ setWait(14.932,19.895)
    $ speak(COUNSELOR, "How can you girls make jokes at a time like this? Your classmate just took his life.")
    show nicole sc3:
        xzoom -1
        xalign 0.58
    $ setWait(19.895,23.232)
    $ speak(NICOLE, "Yeah you were about to take me out on a date, fuck off pedophile!")
    show emt:
        xzoom -1
        off_left
        linear 0.6 xalign 0.13
    $ setWait(23.232,26.485)
    $ speak(EMT, "Pedophile? Was this boy molested to the point of suicide?")
    $ setWait(26.485,31.282)
    $ speak(NICOLE, "No it's just our guidance counselor trying to molest.. me, no big deal.")
    $ setWait(31.282,32.658)
    $ speak(EMT, "Well I should alert the police.")
    show cop:
        xzoom -1
        off_left
        linear 0.4 xalign -.12
    show couns 2:
        xalign -.12
        linear 0.3 off_left
    show emt:
        pause 0.5
        xzoom 1
    $ setWait(32.658,34.827)
    $ speak(COP, "Already here.")
    stop ambient fadeout 2
    jump scene_0123
label scene_0117:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        0.1
        linear 1.5 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0117.mp3")
    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 1.5
    scene school ext 3
    $ setWait(0.376,3.337)
    $ speak(KYLAR, "Aw shit!! My legs are in pieces!!")
    show lynn:
        off_right
        linear 1.45 rightcenterstage
    show nicole sc3:
        off_right
        pause 0.5
        xzoom -1
        linear 2.5 xalign 0.2
        xzoom 1
    $ setWait(3.337,4.756)
    $ speak(LYNN, "Somebody call 911!")
    show emt:
        off_left
        xzoom -1
        linear 2 off_right
        pause 1.5
        off_right
        linear 2 xalign -.12

    show kylar stretch:
        xalign 4.7
        pause 3.5
        linear 2 leftcenterstage

    show lynn:
        rightcenterstage
        pause 1.5
        xzoom -1
    $ setWait(4.756,9.343)
    $ speak(EMT, "Somebody already did, step aside.")
    show lynn:
        xzoom 1


    $ setWait(9.343,12.096)
    $ speak(LYNN, "I'll have to call his parents, how severe is it?")
    show kylar stretch:
        leftcenterstage
    $ setWait(12.096,15.641)
    $ speak(EMT, "I'm no doctor but I don't think he'll ever walk again.")
    $ setWait(15.641,16.392)
    $ speak(KYLAR, "What!?")
    $ setWait(16.392,17.018)
    $ speak(EMT, "Let's go.")
    $ setWait(17.018,20.772)
    $ speak(KYLAR, "But Lacrosse! Will I be able to play Lacrosse!?")
    show lynn:
        pause 2.9
        rightcenterstage
        xzoom -1
        linear 1.7 off_right
    show emt:
        xalign -.12
        xzoom -1
    $ setWait(20.772,24.192)
    $ speak(EMT, "Well if you can't walk...")
    $ setWait(24.192,26.527)
    $ speak(KYLAR, "Oh my god! Nicole! Nicole!")
    hide lynn

    show nicole sc3:
        xzoom -1
        leftcenterstage
    $ setWait(26.527,27.904)
    $ speak(NICOLE, "What? I'm right here.")
    $ setWait(27.904,33.743)
    $ speak(KYLAR, "It's fucked up but I don't think I'll be able to support us as a pro lacrosse player anymore.")
    $ setWait(33.743,35.078)
    $ speak(NICOLE, "That was the plan?")
    $ setWait(35.078,40.792)
    $ speak(KYLAR, "But it doesn't mean anything, we'll figure it out together.. right?")
    menu:
        "I ONLY DATE MEN\nWHO CAN WALK":
            jump scene_0118
        "LIE TO HIM SO IT\nHURTS WORSE LATER":
            jump scene_0119
label scene_0118:
    $ setVoiceTrack("audio/Scenes/0118.mp3")
    scene school ext 3
    show emt:
        xzoom -1
        xalign -.12



    show nicole sc3:
        xzoom -1
        leftcenterstage

    show kylar stretch:
        leftcenterstage
    $ setWait(0.243,3.588)
    $ speak(NICOLE, "Sorry I only date men who can walk.")
    $ setWait(3.588,6.925)
    $ speak(KYLAR, "What? But I did all this for you!")
    $ setWait(6.925,9.052)
    $ speak(NICOLE, "I didn't ask for all this.")
    $ setWait(9.052,11.012)
    $ speak(KYLAR, "But now I can't walk!")
    $ setWait(11.012,12.222)
    $ speak(NICOLE, "Sucks to be you, dude.")
    show kylar stretch:
        leftcenterstage
        linear 4.5 xalign -4.2

    show emt:
        xalign -.12
        linear 0.7 off_left
    $ setWait(12.222,15.183)
    $ speak(KYLAR, "Aaahhhh!!!")
    show lynn:
        off_right
        pause 3
        linear 2.7 rightcenterstage
    $ setWait(15.183,21.523)
    $ speak(EMT, "Alright go!")
    $ setWait(21.523,24.818)
    $ speak(LYNN, "Nicole.. do you need to talk?")
    show nicole sc3:
        xzoom 1
        leftcenterstage
    $ setWait(24.818,28.571)
    $ speak(NICOLE, "About what? How men do stupid shit for you when you're pretty.")
    stop ambient fadeout 6
    show black:
        alpha 0.0
        pause 3
        linear 3 alpha 1.0
    $ setWait(28.571,35.618)
    $ speak(LYNN, "Well I've been there too but-- okay you're fine.")
    jump scene_0122
label scene_0119:
    $ setVoiceTrack("audio/Scenes/0119.mp3")
    scene school ext 3
    show emt:
        xzoom -1
        xalign -.12



    show nicole sc3:
        xzoom -1
        leftcenterstage

    show kylar stretch:
        leftcenterstage
    $ setWait(0.715,4.26)
    $ speak(NICOLE, "Uh.. Kind of. Probably, sure yeah.")
    show kylar stretch:
        leftcenterstage
        linear 4.5 xalign -4.2

    show emt:
        xalign -.12
        linear 0.7 off_left
    $ setWait(4.26,7.597)
    $ speak(KYLAR, "As long as I have you I'll be okay.")
    hide kylar
    hide emt
    show lynn:
        off_right
        pause 2
        linear 3 rightcenterstage
    $ setWait(7.597,13.561)
    $ speak(EMT, "Alright go!")
    $ setWait(13.561,15.313)
    $ speak(LYNN, "So what'd you tell him?")
    show nicole sc3:
        leftcenterstage
        xzoom 1
    $ setWait(15.313,21.903)
    $ speak(NICOLE, "I gave a very loose \"yes\" to being his girlfriend. That should keep him stable in whatever mental ward they ship him off to.")
    $ setWait(21.903,26.741)
    $ speak(LYNN, "Nicole, uh... is there anything you learned today?")
    $ setWait(26.741,31.871)
    $ speak(NICOLE, "That men will do literally anything for sex, but honestly I learned that years ago.")
    $ setWait(31.871,37.46)
    $ speak(LYNN, "So if you knew that, why did you actively encourage him in the first place?")
    $ setWait(37.46,41.631)
    $ speak(NICOLE, "I wanted to see what literally anything looked like.")
    $ setWait(41.631,45.009)
    $ speak(LYNN, "Hm... You're smarter than I was at your age.")
    $ setWait(45.009,46.552)
    $ speak(NICOLE, "Duh, I have internet.")
    $ setWait(46.552,52.767)
    $ speak(LYNN, "Of course. So the school's probably shut down for the rest of the day, where are you headed?")
    stop ambient fadeout 3
    menu:
        "NEED TO GO HOME AFTER THIS SHIT":
            jump scene_0122
        "MAKE USE OF\nTHE KEY HE GAVE ME":
            jump scene_0120
label scene_0120:
    $ setVoiceTrack("audio/Scenes/0120.mp3")
    play ambient "audio/Ambience/neighborhood_ambience_night.mp3" fadein 1.2
    scene onlayer master
    show black
    show house kylar night with Pause(2.5):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.5 zoom .6 truecenter

    scene home kylar
    play ambient "audio/Ambience/House_Night_Ambience.mp3"
    show black onlayer screens:
        alpha 0.3
    show nicole sc3 sly:
        off_left
        linear 5.3 rightstage
    $ setWait(2.504,8.468)
    $ speak(NICOLE, "Really glad I let him give me that key now. If he's in the hospital for a month he won't be missing any of his shit.")
    show drawer
    $ setWait(8.468,14.849)
    $ speak(NICOLE, "Oh my god. There's enough Percocet here to get surgery awake. I'm snagging all of this.")
    show nicole sc3 sly:
        rightstage
        xzoom -1
        linear 5 off_left
    hide drawer
    stop ambient fadeout 6.25
    show black onlayer screens:
        alpha 0.3
        pause 4.5
        linear 2.2 alpha 1
    $ setWait(14.849,22.688)
    $ speak(NICOLE, "How many milligrams to just stop feeling emotions in general?")
    jump end_0121

label end_0121:
    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0121" not in persistent.endings:
        $ persistent.endings.append("end_0121")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0121end with Pause (35.7):
        alpha 1.0
    return

label scene_0122:
    $ setVoiceTrack("audio/Scenes/0122.mp3")
    play ambient "audio/Ambience/exterior_ambience.mp3" fadein 1.2
    scene onlayer master
    show black
    show home nicole ext day with Pause(2.338):
        zoom 0.8 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.338 zoom .85 truecenter

    scene home nicole int
    play ambient "audio/ambience/house_ambience.mp3"
    show nicole sc3:
        xzoom -1
        off_right
        pause 2.4
        linear 2 rightstage
    show mom 3:
        xzoom -1
        leftstage

    $ setWait(2.338,6.133)
    $ speak(MOM, "")
    $ setWait(6.133,8.344)
    $ speak(MOM, "Do I even have to ask?")
    show nicole sc3:
        rightstage
    $ setWait(8.344,9.47)
    $ speak(NICOLE, "Ask what?")
    show mom 3:
        leftstage
        linear 2 leftcenterstage
    $ setWait(9.47,11.305)
    $ speak(MOM, "You know what.")
    $ setWait(11.305,14.35)
    $ speak(NICOLE, "Oh yeah the school security guard's single. Go for it, Mom.")
    show mom 3 angry:
        xzoom -1
        leftcenterstage
    $ setWait(14.35,15.309)
    $ speak(MOM, "Not that!")
    $ setWait(15.309,17.061)
    $ speak(NICOLE, "I didn't fucking do anything.")
    $ setWait(17.061,25.11)
    $ speak(MOM, "A boy jumped off a building to prove his love to you, you had to have done something. This is like the 3rd time now. Did you egg him on?")
    $ setWait(25.11,27.905)
    $ speak(NICOLE, "No...not really, maybe.")
    show mom 3:
        xzoom -1
        leftcenterstage
    $ setWait(27.905,29.24)
    $ speak(MOM, "Of course.")
    $ setWait(29.24,33.577)
    $ speak(NICOLE, "Okay this shouldn't even be the main issue today, the school counselor tried having sex with me.")
    $ setWait(33.577,41.502)
    $ speak(MOM, "You expect me to believe that? A boy literally kills himself the same day a teacher molests you? You must be the least lucky girl on earth.")
    show nicole sc3:
        xzoom -1
        rightstage
        linear 1.23 rightcenterstage
    $ setWait(41.502,45.422)
    $ speak(NICOLE, "Uh yeah I am. And he didn't even kill himself, he's fine in the hospital.")
    $ setWait(45.422,49.218)
    $ speak(MOM, "I just got off the phone with your principal and he was pronounced dead 20 minutes ago.")
    $ setWait(49.218,51.679)
    $ speak(NICOLE, "What? How? It was just his legs.")
    $ setWait(51.679,55.85)
    $ speak(MOM, "His pelvis shattered into his intestines, he internally bled out.")
    $ setWait(55.85,57.393)
    $ speak(NICOLE, "Oh my god.")
    $ setWait(57.393,59.603)
    $ speak(MOM, "Is it finally setting in?")
    $ setWait(59.603,61.026)
    $ speak(NICOLE, "Yeah...")
    $ setWait(61.026,65.526)
    $ speak(NICOLE, "I forgot to go to his house and steal his Percocet, his parents probably threw it out by now!")
    stop ambient fadeout 5.2
    show black:
        alpha 0.0
        pause 3.5
        linear 2 alpha 1.0
    $ setWait(65.526,70.947)
    $ speak(MOM, "Ugh.. you better hope they don't sue us over this.")
    jump scene_0123
label scene_0123:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 2.6 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0123.mp3")
    scene school int 1
    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 2
    show guy_2 color2:
        leftcenterstage
        xzoom -1
    show crispin sc3 unhappy:
        rightcenterstage
    $ setWait(0.101,3.499)
    $ speak(GUY_2, "Yeah this place is wild after that.")
    $ setWait(3.499,5.626)
    $ speak(CRISPIN, "I can't even understand how it happened.")
    show nicole sc4:
        off_left
        linear 2 leftstage

    show guy_2 color2 scared:
        pause 0.6
        xzoom 1

    $ setWait(5.626,9.004)
    $ speak(NICOLE, "Hey do you guys know where the janitor's closet is? I'm trying to sell him something.")
    $ setWait(9.004,10.047)
    $ speak(CRISPIN, "Sorry I don't know anything.")
    show crispin sc3 unhappy:
        rightcenterstage
        pause 0.2
        xzoom -1
        linear 1.2 off_farright

    show guy_2 color2 scared:
        leftcenterstage
        pause 0.4
        xzoom -1
        linear 1.1 off_right


    $ setWait(10.047,12.842)
    $ speak(GUY_2, "Yeah couldn't tell ya, bye.")
    hide crispin
    hide guy_2
    show nicole sc4:
        leftstage
        linear 2 leftcenterstage
    show jeffery sc3:
        off_right
        linear 3 rightcenterstage
    $ setWait(12.842,14.885)
    $ speak(NICOLE, "...The fuck was that?")
    $ setWait(14.885,16.303)
    $ speak(NICOLE, "Hey anime kid do you know--")
    show jeffery sc3:
        rightcenterstage
        pause 0.1
        xzoom -1
        linear 0.75 off_right
    $ setWait(16.303,19.14)
    $ speak(JEFFERY, "Agh! I'm sorry I'll go.")
    hide jeffery
    $ setWait(19.14,20.099)
    $ speak(NICOLE, "...Why?")
    show jecka sc7:
        off_right
        linear 2 rightcenterstage
    $ setWait(20.099,21.475)
    $ speak(JECKA, "There you are!")
    $ setWait(21.475,23.435)
    $ speak(NICOLE, "Hey, why's everyone avoiding me?")
    $ setWait(23.435,27.439)
    $ speak(JECKA, "Uh the only word on the street is you manipulated Kylar into killing himself.")
    $ setWait(27.439,28.816)
    $ speak(NICOLE, "I barely did anything.")
    $ setWait(28.816,32.153)
    $ speak(JECKA, "Oh my god don't get defensive, I'm on your side, like half the girls are.")
    $ setWait(32.153,34.238)
    $ speak(NICOLE, "Why? How? He didn't even know me.")
    $ setWait(34.238,43.914)
    $ speak(JECKA, "Exactly! All he liked you for was looks, meaning you're pretty enough that a boy would literally die for you. It's like awesome, I wanna be you, what's your secret?")
    $ setWait(43.914,47.751)
    $ speak(NICOLE, "Secret? It's... I just told him to work for it, that's it.")
    $ setWait(47.751,52.131)
    $ speak(JECKA, "Yeah I tell guys that too, they aren't jumping off buildings for me!")
    $ setWait(52.131,55.009)
    $ speak(NICOLE, "This is so not what I thought would happen after this.")
    $ setWait(55.009,63.142)
    $ speak(JECKA, "So many girls are just happy over this. Like I know it's bad cause he's dead or whatever, but like honestly fuck him. He was an asshole the world's better off.")
    $ setWait(63.142,64.977)
    $ speak(NICOLE, "I don't disagree with you.")
    show girl_2 color2:
        off_right
        linear 1.3 rightstage
    $ setWait(64.977,67.646)
    $ speak(GIRL_2, "Hi, Nicole! Could I ask you something?")
    show jecka sc7:
        xzoom -1
    $ setWait(67.646,70.816)
    $ speak(JECKA, "Yeah ask her anything! We're kinda best friends by the way.")
    $ setWait(70.816,76.614)
    $ speak(GIRL_2, "Oh well I was just wondering if it's okay if I put my hair up like yours? --If you're okay with that.")
    $ setWait(76.614,78.699)
    $ speak(NICOLE, "It's a free police-state, do what you want.")
    show girl_2 color2:
        rightstage
        pause 1.65
        xzoom -1
        linear 1 off_right
    $ setWait(78.699,81.368)
    $ speak(GIRL_2, "Awesome thanks, bye!")
    show jecka sc7:
        xzoom 1
    $ setWait(81.368,83.245)
    $ speak(JECKA, "You saw that.")
    hide girl_2
    $ setWait(83.245,84.205)
    $ speak(NICOLE, "Yeah?")
    show jecka sc7:
        rightcenterstage
        linear 0.5 xalign 0.58
    $ setWait(84.205,92.087)
    $ speak(JECKA, "You gotta do something with this, get famous with it. Like you could be one of those famous Youtube girls. \"Hey guys I'm so hot boys kill themselves over me.\"")
    $ setWait(92.087,94.882)
    $ speak(NICOLE, "I was with you on everything except famous.")
    show jecka sc7 unhappy:
        xalign 0.58
    $ setWait(94.882,96.3)
    $ speak(JECKA, "You don't wanna be famous?")
    $ setWait(96.3,99.261)
    $ speak(NICOLE, "No just, no one on Youtube's famous famous.")
    show jecka sc7:
        xalign 0.58
    $ setWait(99.261,102.89)
    $ speak(JECKA, "Well I know that, like just Youtube famous. Come on!")
    menu:
        "MAKE A VLOG ABOUT IDIOT KILLING HIMSELF":
            jump scene_0124
        "EXERCISE YOUR NEWFOUND POWER ANOTHER WAY":
            jump scene_0125
label scene_0124:
    $ setVoiceTrack("audio/Scenes/0124.mp3")
    scene school int 1
    show nicole sc4 sly:
        leftcenterstage

    show jecka sc7:
        xalign 0.58
    $ setWait(0.28,3.297)
    $ speak(NICOLE, "Alright, but I don't have a camera or anything.")
    $ setWait(3.297,6.425)
    $ speak(JECKA, "We'll just record it at my house, I have a mac and everything.")
    $ setWait(6.425,8.427)
    $ speak(NICOLE, "You wanna just skip right now and do that?")
    show jecka sc7:
        xalign 0.58
        pause 1.45
        xzoom -1
        linear 1.2 off_right

    show nicole sc4 sly:
        leftcenterstage
        pause 1.7
        linear 1.4 off_right
    $ setWait(8.427,12.055)
    $ speak(JECKA, "Fucking of course, let's go!")
    stop ambient fadeout 2
    jump end_0126
label scene_0125:
    $ setVoiceTrack("audio/Scenes/0125.mp3")
    scene school int 1
    show nicole sc4:
        leftcenterstage

    show jecka sc7:
        xalign 0.58
    $ setWait(0.304,3.924)
    $ speak(NICOLE, "Well hold on, I might have a way easier idea here.")
    $ setWait(3.924,5.092)
    $ speak(JECKA, "Okay let's see it.")
    $ setWait(5.092,6.843)
    $ speak(NICOLE, "Call over the weird nerdy kid.")
    show jecka sc7:
        xzoom -1
        xalign 0.58
        linear 0.5 xalign .8
    $ setWait(6.843,9.513)
    $ speak(JECKA, "Jeffery! Can you help me hold my books?")
    show jeffery sc3 happy:
        off_right
        linear 0.5 rightstage
    $ setWait(9.513,13.225)
    $ speak(JEFFERY, "Huh! Yeah of course, anything for you! Where's the books?")
    show nicole sc4 mean:
        leftcenterstage
        linear 1.4 xalign 0.57
    $ setWait(13.225,14.851)
    $ speak(NICOLE, "Hi Jeffery.")
    show jeffery sc3:
        rightstage
        linear 0.06 xalign 1.02
        linear 0.06 xalign .98
        linear 0.06 xalign 1.02
        linear 0.06 xalign .98
        linear 0.06 xalign 1.02
        linear 0.06 xalign .98
        linear 0.06 rightstage
    $ setWait(14.851,18.021)
    $ speak(JEFFERY, "Ugh! N-Nicole, hi there.")
    show nicole sc4 mean:
        xalign 0.57
        linear 0.7 xalign 0.79

    show jecka sc7:
        xalign .8
        pause 0.2
        linear 0.6 xalign .58
    $ setWait(18.021,22.818)
    $ speak(NICOLE, "What's wrong, Jeffery? Just looking for a new friend to chat with. Am I no good?")
    $ setWait(22.818,33.161)
    $ speak(JEFFERY, "Uh no you're fine! It's just.. I'm afraid of you. Afraid you'll use your emotional prowess to manipulate me into killing myself.")
    $ setWait(33.161,35.372)
    $ speak(NICOLE, "Is that what those boys are saying?")
    $ setWait(35.372,37.207)
    $ speak(JEFFERY, "Yes, you'd be correct.")
    $ setWait(37.207,38.709)
    $ speak(NICOLE, "Well guess what.")
    $ setWait(38.709,39.293)
    $ speak(JEFFERY, "...What?")

    $ setWait(39.293,40.043)
    $ speak(NICOLE, "They're right.")
    show jeffery sc3 emb:
        rightstage
        linear 0.06 xalign 1.02
        linear 0.06 xalign .98
        linear 0.06 xalign 1.02
        linear 0.06 xalign .98
        linear 0.06 xalign 1.02
        linear 0.06 xalign .98
        linear 0.06 rightstage
    $ setWait(40.043,40.919)
    $ speak(JEFFERY, "Ah!")
    $ setWait(40.919,43.547)
    $ speak(NICOLE, "You don't wanna fall in love with me do you?")
    show jeffery sc3 emb:
        rightstage
        pause .8
        xalign 1.05
        xzoom -1
        pause 1
        rightstage
        xzoom 1
    $ setWait(43.547,46.466)
    $ speak(JEFFERY, "Yes! I mean no-- I mean I don't know!")
    show nicole sc4 mean:
        xalign 0.79
        pause 9
        linear 0.1 xalign .84

    show jeffery sc3 emb:
        rightstage
        pause 9.06
        linear 0.1 xalign 1.05

    $ setWait(46.466,56.435)
    $ speak(NICOLE, "You're a smart boy, right? Let's make a deal. You do all my homework and slip me every test answer, and I won't force you to kill yourself.")
    show nicole sc4 mean:
        xalign .84

    show jeffery sc3:
        xalign 1.05
    $ setWait(56.435,63.15)
    $ speak(JEFFERY, "R-really? You'd do that for me? I never thought a girl would be this nice to me.")
    $ setWait(63.15,65.152)
    $ speak(NICOLE, "Say yes before I change my mind.")
    show jeffery sc3 emb:
        xalign 1.05
        pause 3.2
        xzoom -1
        linear 0.6 off_farright
    $ setWait(65.152,70.949)
    $ speak(JEFFERY, "Uh! Of course, I'll get right on it! See ya tomorrow!")
    $ setWait(70.949,73.91)
    $ speak(JECKA, "I don't believe what I just saw.")
    show nicole sc4:
        xalign .88
        xzoom -1
        linear 5 leftstage
        xzoom 1
    $ setWait(73.91,78.457)
    $ speak(NICOLE, "Yeah I don't believe it either but there's no way this'll last.")
    show jecka sc7 unhappy:
        xzoom 1
    $ setWait(78.457,81.418)
    $ speak(JECKA, "...But seriously is it like your whole emo look they're into or what?")
    $ setWait(81.418,85.931)
    $ speak(NICOLE, "Yeah long flowing ponytail, very emo.")
    stop ambient fadeout 2
    jump end_0127

label end_0126:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0126" not in persistent.endings:
        $ persistent.endings.append("end_0126")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0126end with Pause (26.8):
        alpha 1.0
    return

label end_0127:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0127" not in persistent.endings:
        $ persistent.endings.append("end_0127")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0127end with Pause (28.7):
        alpha 1.0
    return

label scene_0128:
    $ setVoiceTrack("audio/Scenes/0128.mp3")

    play ambient "audio/Ambience/Neighborhood_Ambience_Night.mp3" fadein 1
    scene onlayer master
    show black

    show title_months onlayer screens:
        alpha 0.0
        linear .2 alpha 1.0

    show home nicole ext night with Pause(3.252):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 3.252 zoom .6 truecenter

    scene home nicole int
    hide title_months onlayer screens
    play ambient "audio/Ambience/House_Night_Ambience.mp3"
    show mom 4:
        xalign 1.2
        linear 2.7 rightcenterstage

    show nicole athome3:
        leftcenterstage
    $ setWait(3.252,7.548)
    $ speak(MOM, "So it's been a few months since we moved, how's school going?")
    $ setWait(7.548,11.386)
    $ speak(NICOLE, "Like academically or socially?")
    $ setWait(11.386,12.971)
    $ speak(MOM, "Everything, anything.")
    show nicole athome3 smile:
        leftcenterstage
    $ setWait(12.971,16.099)
    $ speak(NICOLE, "Honestly, it's going pretty good.")
    show mom 4 smile:
        rightcenterstage
    $ setWait(16.099,20.186)
    $ speak(MOM, "Oh that's great to hear, I know moving schools can be hard.")
    $ setWait(20.186,29.487)
    $ speak(NICOLE, "And if I cared, it absolutely would be. But Mom, I figured out that if you just don't engage with other people's emotions or desires, nothing's a burden.")
    show mom 4:
        rightcenterstage
    $ setWait(29.487,30.78)
    $ speak(MOM, "Excuse me?")
    $ setWait(30.78,32.615)
    $ speak(NICOLE, "Like I'll put it like this...")
    $ setWait(32.615,42.583)
    $ speak(NICOLE, "...Anytime a guy asks for my company, asks me out, asks for anything... and I make decisions entirely for myself not concerned with their feelings, there's no stress.")
    show mom 4 concerned:
        rightcenterstage
    $ setWait(42.583,45.92)
    $ speak(MOM, "Honey that sounds a little mean-spirited, don't you think?")
    show nicole athome3:
        leftcenterstage
    $ setWait(45.92,54.345)
    $ speak(NICOLE, "Yeah well what's the alternative? Being used to do shit? People, especially men, are the perfect pawns when you don't give a fuck about them or whatever they want.")
    $ setWait(54.345,59.851)
    $ speak(MOM, "Ugh I won't argue.. I'll just hope you learn how to interact like a human being when you're a senior.")
    show nicole athome3 angry:
        leftcenterstage
    $ setWait(59.851,66.19)
    $ speak(NICOLE, "So you're telling me it's a requirement for women to be pushovers? Or we're sociopathic? What the fuck happened to feminism, Mom?")
    show mom 4:
        rightcenterstage
    $ setWait(66.19,71.904)
    $ speak(MOM, "Nicole, I don't know any woman who actively considers feminism. We vote and work, it's just a fun thing to say.")
    $ setWait(71.904,75.033)
    $ speak(NICOLE, "Okay well fuck feminism, I'm starting Nicoleism!")
    $ setWait(75.033,76.2)
    $ speak(MOM, "Nicoleism?")
    $ setWait(76.2,80.788)
    $ speak(NICOLE, "Yeah, the main concept is girls removing all emotional attachment from anyone.")
    $ setWait(80.788,84.375)
    $ speak(MOM, "Oh I'm sure you'll meet a nice boy soon and you'll be all over this.")
    $ setWait(84.375,90.506)
    $ speak(NICOLE, "How can I meet a nice boy when all men are just rapists and pedophiles? Is fucking kids nice, Mom?")
    stop ambient fadeout 5
    show black:
        alpha 0.0
        pause 2.2
        linear 2 alpha 1.0
    show mom 4:
        rightcenterstage
        linear 3.8 off_left

    $ setWait(90.506,97.075)
    $ speak(MOM, "This conversation is over.")
    jump scene_0130
label scene_0129:
    $ setVoiceTrack("audio/Scenes/0129.mp3")
    play ambient "audio/Ambience/Neighborhood_Ambience_Night.mp3" fadein 1
    scene onlayer master
    show black

    show title_months onlayer screens:
        alpha 0.0
        linear .2 alpha 1.0

    show home nicole ext night with Pause(3.166):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 3.166 zoom .6 truecenter

    scene home nicole int
    hide title_months onlayer screens
    play ambient "audio/Ambience/House_Night_Ambience.mp3"
    show nicole athome3:
        rightcenterstage

    show mom 4:
        xzoom -1
        xalign -0.13
        linear 2 leftcenterstage
    $ setWait(3.166,4.542)
    $ speak(MOM, "Nicole?")
    $ setWait(4.542,7.67)
    $ speak(NICOLE, "I'm trying to make a depression playlist on iTunes, what is it?")
    $ setWait(7.67,12.258)
    $ speak(MOM, "Well nothing really, I'm just wondering why you've been so exhausted lately?")
    show nicole athome3 angry:
        rightcenterstage
        xzoom -1
    $ setWait(12.258,13.634)
    $ speak(NICOLE, "People, Mom.")
    $ setWait(13.634,16.637)
    $ speak(MOM, "You're being nice, right? Trying to get along?")
    $ setWait(16.637,23.144)
    $ speak(NICOLE, "Yeah, and I'm pretty sure that's my problem. Never putting up a fight. Never telling men I'm not their emotional wheelchair.")
    show mom 4 concerned:
        xzoom -1
        leftcenterstage
    $ setWait(23.144,32.737)
    $ speak(MOM, "Well sweetie, I'm not sure if being confrontational is the key to happiness. You're a beautiful girl, don't have an ugly personality, towards anyone.")
    $ setWait(32.737,38.159)
    $ speak(NICOLE, "So I should like spread myself thin so anyone can have a place in my life?")
    $ setWait(38.159,44.999)
    $ speak(MOM, "Don't put it so negatively, all I'm saying is; be inclusive. Give people a chance.")
    $ setWait(44.999,46.751)
    $ speak(NICOLE, "What if they're bad people?")
    $ setWait(46.751,50.046)
    $ speak(MOM, "I don't believe in anyone being inherently bad.")
    $ setWait(50.046,54.717)
    $ speak(NICOLE, "Yeah I guess the pedophiles trying to abduct me on MySpace are just misunderstood.")
    $ setWait(54.717,60.598)
    $ speak(MOM, "Always a negative spin-- Just promise you'll try. Try to be nice and make time for people.")
    $ setWait(60.598,65.311)
    $ speak(MOM, "The connections you start early come in handy later on. Don't screw up here.")
    $ setWait(65.311,66.896)
    $ speak(NICOLE, "Ugh fine.")
    show mom 4 smile:
        xzoom -1
        leftcenterstage
        pause 1.9
        xzoom 1
        linear 4 off_left
    $ setWait(66.896,71.984)
    $ speak(MOM, "Thank you. I promise it'll pay off.")
    stop ambient fadeout 5
    show black:
        alpha 0.0
        pause 2.3
        linear 2 alpha 1.0
    $ setWait(71.984,78.154)
    $ speak(NICOLE, "...I'll be your enabling little princess.")
    jump scene_0162
label scene_0130:
    $ setVoiceTrack("audio/Scenes/0130.mp3")
    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 1.5
    scene onlayer master
    show black

    show title_october2008 onlayer screens:
        alpha 0.0
        linear .2 alpha 1.0

    show school front with Pause(2.664):
        zoom 1.0 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.664 zoom 1.1 truecenter
    scene photo classroom
    hide title_october2008 onlayer screens
    play ambient "audio/Ambience/Classroom_Ambience.mp3"
    show mr_white:
        rightstage

    show jecka sc4 unhappy:
        xzoom -1
        xalign -0.1

    show girl_4:
        rightcenterstage
        xzoom -1

    show crispin sc4:
        xzoom -1
        xalign 0.41

    show nicole sc6:
        xalign .17
        xzoom -1
    $ setWait(2.664,9.379)
    $ speak(MR_WHITE, "And so you see, the aperture actually gets wider the lower the F-stop gets.")
    $ setWait(9.379,11.089)
    $ speak(NICOLE, "Did I really forget my eyeliner?")
    $ setWait(11.089,13.174)
    $ speak(MR_WHITE, "Ahem... Ahem!")
    show nicole sc6:
        xalign .1
        xzoom 1
    $ setWait(13.174,15.593)
    $ speak(NICOLE, "Dude you really need that cough looked at, it's kind of annoying.")
    $ setWait(15.593,18.596)
    $ speak(MR_WHITE, "This isn't cosmetics class, Nicole...")
    $ setWait(18.596,19.389)
    $ speak(NICOLE, "I know that.")
    $ setWait(19.389,24.06)
    $ speak(MR_WHITE, "So pay attention to the photography lecture in photography class.")
    show nicole sc6 angry:
        xalign .17
        xzoom -1
    $ setWait(24.06,26.104)
    $ speak(NICOLE, "I'll be done in like 2 seconds just calm down.")
    show mr_white:
        rightstage
        linear 1.2 xalign 0.45

    show girl_4:
        rightcenterstage
        pause 0.5
        linear 0.7 rightstage
        xzoom 1

    show crispin sc4 unhappy:
        xalign 0.41
        pause 0.75
        linear 0.6 xalign 0.76
        xzoom 1

    $ setWait(26.104,28.022)
    $ speak(MR_WHITE, "Now, Nicole!")
    menu:
        "PASSIVE-AGGRESSIVE\nEYE ROLL":
            jump scene_0131
        "HE CAN'T TELL YOU\nWHAT TO DO":
            jump scene_0132
label scene_0131:
    $ setVoiceTrack("audio/Scenes/0131.mp3")
    scene photo classroom
    show mr_white:
        xalign 0.45

    show crispin sc4 unhappy:
        xalign 0.76

    show girl_4:
        rightstage

    show nicole sc6:
        xalign .1

    show jecka sc4 unhappy:
        xzoom -1
        xalign -0.1
    $ setWait(0.035,1.786)
    $ speak(NICOLE, "Okay fine.")
    $ setWait(1.786,3.538)
    $ speak(MR_WHITE, "Wonderful, as I was saying--")
    show jecka sc4 angry:
        xalign -.1
        xzoom -1
        linear .5 xalign 0.19

    show nicole sc6 surprised:
        xalign .1
        pause 0.35
        linear 0.6 xalign -0.12
    $ setWait(3.538,5.332)
    $ speak(JECKA, "You can't talk like that to her!")
    $ setWait(5.332,7.917)
    $ speak(MR_WHITE, "I can talk any way I'd like, Jessica.")
    $ setWait(7.917,14.966)
    $ speak(JECKA, "That's not my name! See? You don't respect any of the girls. A guy could just whip his dick out in here and you'd just politely say \"that's enough\".")
    $ setWait(14.966,17.26)
    $ speak(MR_WHITE, "You're on thin ice right now!")
    $ setWait(17.26,21.765)
    $ speak(JECKA, "You're on your fourth wife right now cause you couldn't make it as a photographer.")
    $ setWait(21.765,22.932)
    $ speak(NICOLE, "I heard it was only 3.")
    $ setWait(22.932,26.353)
    $ speak(MR_WHITE, "That's it! Both of you have detention this afternoon!")
    show nicole sc6:
        xalign -0.08
        xzoom -1
        linear 2 off_left
    $ setWait(26.353,27.604)
    $ speak(NICOLE, "Great...")
    stop ambient fadeout 2
    jump scene_0133
label scene_0132:
    $ setVoiceTrack("audio/Scenes/0132.mp3")
    scene photo classroom
    show mr_white:
        xalign 0.45

    show crispin sc4 unhappy:
        xalign 0.76

    show girl_4:
        rightstage

    show jecka sc4 unhappy:
        xzoom -1
        xalign -0.1

    show nicole sc6 angry:
        xalign .1
    $ setWait(0.046,3.633)
    $ speak(NICOLE, "Now nothing, literally go fuck yourself.")
    $ setWait(3.633,11.057)
    $ speak(MR_WHITE, "How dare you! How dare you disrupt my lecture, it's disrespectful to me and your classmates!")
    $ setWait(11.057,16.395)
    $ speak(NICOLE, "You can't trick anyone here into being mad at me when no one gives a shit about your class in the first place.")
    $ setWait(16.395,23.111)
    $ speak(MR_WHITE, "Well how would you like a failing grade? How would all of you like a failing grade?")
    $ setWait(23.111,25.863)
    $ speak(JECKA, "I mean... I guess that's fine it's an elective.")
    show crispin sc4:
        xalign 0.76
    $ setWait(25.863,29.117)
    $ speak(CRISPIN, "Yeah Mr. White you can't keep us from graduating. You tell 'em, Nicole!")
    $ setWait(29.117,31.494)
    $ speak(NICOLE, "Shut the fuck up you finger skateboard bitch.")
    show crispin sc4 unhappy:
        xalign 0.76
    $ setWait(31.494,32.954)
    $ speak(CRISPIN, "Dude I was just trying to help.")
    $ setWait(32.954,34.372)
    $ speak(NICOLE, "Yeah you were trying something.")
    $ setWait(34.372,39.293)
    $ speak(MR_WHITE, "How would you like a visit to the counselors office? The principal's office?")
    show nicole sc6:
        xalign .1
    $ setWait(39.293,43.422)
    $ speak(NICOLE, "Hey if you think not listening to you talk is discipline then I'm gone no problem.")
    show mr_white:
        xalign 0.45
        linear 1 xalign 0.39

    show nicole sc6:
        xalign 0.1
        pause 1.6
        xzoom -1
        linear 2 off_left
    $ setWait(43.422,46.592)
    $ speak(MR_WHITE, "Out! Now!")
    stop ambient fadeout 2
    jump scene_0134
label scene_0133:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.8 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0133.mp3")

    scene office 2
    show lynn:
        xalign 0.88

    show nicole sc6:
        leftstage

    show jecka sc4 unhappy:
        leftcenterstage
        xzoom -1
    play ambient "audio/ambience/office_ambience.mp3" fadein 1.2
    $ setWait(0.062,2.498)
    $ speak(LYNN, "I feel like I see you two every week now.")
    $ setWait(2.498,4.583)
    $ speak(JECKA, "Swear to god, wasn't even our fault.")
    $ setWait(4.583,10.256)
    $ speak(NICOLE, "What she said, except for the swear to god part. I'd like to think god isn't keeping tabs on 17 year old girls.")
    $ setWait(10.256,15.135)
    $ speak(LYNN, "Oh so in your spiritual worldview God only keeps tabs on fully matured women?")
    show jecka sc4:
        leftcenterstage
        xzoom -1
    $ setWait(15.135,17.763)
    $ speak(JECKA, "Yeah, Ms. Lynn. Back that divine ass up!")
    show lynn:
        xalign 0.88
        linear 0.2 rightcenterstage

    show jecka sc4 unhappy:
        leftcenterstage
        pause 0.15
        linear 0.2 xalign 0.3
    $ setWait(17.763,24.228)
    $ speak(LYNN, "Enough! When it comes to repeat offenders it's no longer a them problem, it's a you problem.")
    $ setWait(24.228,25.104)
    $ speak(NICOLE, "And?")
    $ setWait(25.104,26.981)
    $ speak(JECKA, "Yeah really don't see what you're getting at.")
    $ setWait(26.981,32.736)
    $ speak(LYNN, "Would either of you like to explain to me why you're in my office from photography yet again?")
    show jecka sc4 unhappy:
        xalign 0.3
        xzoom 1
    $ setWait(32.736,33.612)
    $ speak(JECKA, "...Nicole?")
    show nicole sc6 angry:
        leftstage
    $ setWait(33.612,34.28)
    $ speak(NICOLE, "What!?")
    $ setWait(34.28,37.074)
    $ speak(LYNN, "Yes Nicole, do tell.")
    menu:
        "LIE, LIE, AND LIE SOME MORE":
            jump scene_0137
        "PRETEND TO BE SORRY TO GET BACK TO CLASS":
            jump scene_0146
label scene_0134:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.8 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0134.mp3")
    scene office 1
    play ambient "audio/ambience/office_ambience.mp3" fadein 1.2
    show couns 2:
        rightstage

    show nicole sc6:
        centerstage
    $ setWait(0.044,1.996)
    $ speak(COUNSELOR, "Again, Nicole?")
    $ setWait(1.996,5.041)
    $ speak(NICOLE, "Can we just pretend you said a lot of stuff so I can leave early?")
    $ setWait(5.041,8.461)
    $ speak(COUNSELOR, "The principal ordered for you to be in this room for 1 hour.")
    $ setWait(8.461,12.632)
    $ speak(NICOLE, "Well I order no mayo at Dairy Queen but you still see them slapping the shit on.")
    $ setWait(12.632,16.302)
    $ speak(COUNSELOR, "And what do you mean by that? How are you feeling?")
    $ setWait(16.302,24.143)
    $ speak(NICOLE, "I'm saying if a whole company like them can't get my order right then what's 1 guy like you? Mistakes happen, they can try again after the next soccer practice.")
    $ setWait(24.143,26.229)
    $ speak(COUNSELOR, "I think we got a bit sidetracked here.")
    $ setWait(26.229,29.649)
    $ speak(NICOLE, "No not just sidetracked, I fucking derailed this shit.")
    $ setWait(29.649,38.491)
    $ speak(COUNSELOR, "Talking out of turn in class, bullying classmates, talking back to faculty.. Is this really the legacy you want to leave here?")
    menu:
        "SHED SOME LIGHT ON EVERYONE ELSE":
            jump scene_0135
        "IT'S HIGH SCHOOL WHO GIVES A SHIT?":
            jump scene_0136
label scene_0135:
    $ setVoiceTrack("audio/Scenes/0135.mp3")
    scene office 1
    show couns 2:
        rightstage

    show nicole sc6 angry:
        centerstage
    $ setWait(0.089,4.26)
    $ speak(NICOLE, "Say that to all the guys who go here. It's like a coed prison without tattoos.")
    $ setWait(4.26,10.224)
    $ speak(COUNSELOR, "Do you think it's a tad irresponsible to point fingers at others when you're the one in question here?")
    $ setWait(10.224,15.313)
    $ speak(NICOLE, "Aren't you mister child psychologist? Like trauma and all that shapes who we are?")
    $ setWait(15.313,20.651)
    $ speak(COUNSELOR, "Well yes I have several degrees in pediatric psychology, what's your point?")
    $ setWait(20.651,27.992)
    $ speak(NICOLE, "Every dude here is like a rapist, or a drug addict, or trying to turn you into a drug addict. Have you tried stopping the problem at its source?")
    $ setWait(27.992,34.415)
    $ speak(COUNSELOR, "I understand some of the male students here can be problematic, but you can always get help from a teacher--")
    $ setWait(34.415,37.23)
    $ speak(NICOLE, "The teachers are trying to fuck me too, you're all psychotic!")
    $ setWait(37.23,44.884)
    $ speak(NICOLE, "A few months ago Mr. Burleday was really feeling up one of my friends, and just last week the coach was staring down my shirt during push-up tests.")
    $ setWait(44.884,55.186)
    $ speak(COUNSELOR, "I try to level with all my students so.. can you really blame him? Some of your attire has been quite.. low cut here.")
    show nicole sc6:
        centerstage
    $ setWait(55.186,56.395)
    $ speak(NICOLE, "Go on..")
    $ setWait(56.395,63.194)
    $ speak(COUNSELOR, "To be honest I've had trouble looking away the entire time you've been here. You're a beautiful young woman.")
    show nicole sc6 surprised:
        pause 1.2
        xzoom -1
    $ setWait(63.194,66.405)
    $ speak(NICOLE, "Are you kidding me right now-- where's the hidden camera what show is this?")
    $ setWait(66.405,67.615)
    $ speak(COUNSELOR, "What're you talking about?")
    show nicole sc6:
        xzoom 1
    $ setWait(67.615,73.371)
    $ speak(NICOLE, "You're like acting for a prank show, right? I'm waiting for someone more attractive than you to walk in so I can pretend to laugh.")
    $ setWait(73.371,75.373)
    $ speak(COUNSELOR, "Nicole, there's no prank here.")
    $ setWait(75.373,78.25)
    $ speak(NICOLE, "Oh so you're just seriously a pedophile, awesome.")
    show couns 2 smile:
        rightstage
        linear 3.5 xalign 0.78
    $ setWait(78.25,82.588)
    $ speak(COUNSELOR, "Last year did we ever have our little chat on social constructs?")
    show nicole sc6 angry:
        centerstage
        xzoom -1
        linear 2.9 off_left
    $ setWait(82.588,83.965)
    $ speak(NICOLE, "I'm leaving.")
    stop ambient fadeout 2
    jump scene_0146
label scene_0136:
    $ setVoiceTrack("audio/Scenes/0136.mp3")
    scene office 1
    show couns 2:
        rightstage

    show nicole sc6:
        centerstage
    $ setWait(0.041,2.21)
    $ speak(NICOLE, "I'm sorry, legacy?")
    show couns 2 smile:
        rightstage
    $ setWait(2.21,8.967)
    $ speak(COUNSELOR, "Yes, your mark, your impact left on the student body. Graduation's only a few months away, y'know.")
    $ setWait(8.967,18.435)
    $ speak(NICOLE, "See I'm glad you brought that up. I will literally never see any of these people again after graduation. There's no point in socially trying with anyone here.")
    $ setWait(18.435,22.189)
    $ speak(COUNSELOR, "You must have someone you'd like to stay in touch with after graduation.")
    $ setWait(22.189,23.148)
    $ speak(NICOLE, "Nope.")
    $ setWait(23.148,25.108)
    $ speak(COUNSELOR, "Not even your friend Jessica?")
    $ setWait(25.108,31.072)
    $ speak(NICOLE, "Jecka's like okay but I'm not going out of my way to hang out with her. Isn't legacy for like a major career or something?")
    $ setWait(31.072,32.699)
    $ speak(COUNSELOR, "Your high school career.")
    $ setWait(32.699,38.413)
    $ speak(NICOLE, "Oh is this a career now? What's my salary? A 2 dollar lunch and 20 years of sexual harassment trauma?")
    $ setWait(38.413,44.711)
    $ speak(COUNSELOR, "Such pessimism at such a young age, when you're an adult you learn how to truly love life.")
    $ setWait(44.711,52.761)
    $ speak(NICOLE, "Oh I'm sure there's tons of life to love, none of it having anything to do with this high school. Why would I care what some kid sitting 2 rows back from me thinks?")
    $ setWait(52.761,59.517)
    $ speak(COUNSELOR, "It's not about right now, it's the tons of fun memories you can revel in years after college.")
    $ setWait(59.517,65.857)
    $ speak(NICOLE, "Okay... um. I know you work here and employee culture keeps your checks signed but..")
    $ setWait(65.857,72.03)
    $ speak(NICOLE, "Anyone well into their 20's still thinking about how high school was is a fucking waste of space.")
    $ setWait(72.03,78.453)
    $ speak(COUNSELOR, "Perhaps I should introduce you to some of our class of '87 alumni. Many of them are teachers here today.")
    $ setWait(78.453,81.915)
    $ speak(NICOLE, "So they're the lower middle class of '87? No thanks.")
    stop ambient fadeout 2
    jump scene_0146
label scene_0137:
    $ setVoiceTrack("audio/Scenes/0137.mp3")
    scene office 2
    show lynn:
        rightcenterstage
    show jecka sc4 unhappy:
        xalign 0.3
        xzoom -1

    show nicole sc6:
        leftstage
    $ setWait(0.048,2.508)
    $ speak(NICOLE, "He didn't already tell you?")
    $ setWait(2.508,6.721)
    $ speak(LYNN, "Oh he did, I'm just curious to hear your side of the story.")
    $ setWait(6.721,8.431)
    $ speak(NICOLE, "And Mr. White said?")
    $ setWait(8.431,11.684)
    $ speak(LYNN, "Said you were talking out of turn with extreme vulgarity.")
    $ setWait(11.684,14.979)
    $ speak(NICOLE, "Well yeah, you would too if he was groping you all over mid-lecture.")
    $ setWait(14.979,15.98)
    $ speak(LYNN, "Excuse me?")
    show jecka sc4 surprised:
        xzoom 1
    $ setWait(15.98,16.814)
    $ speak(JECKA, "Yeah what?")
    $ setWait(16.814,20.777)
    $ speak(NICOLE, "Mr. White is a pervert and he's been pulling this shit for like years now.")
    show jecka sc4 unhappy:
        xzoom 1
    $ setWait(20.777,21.778)
    $ speak(LYNN, "Really now?")
    $ setWait(21.778,22.987)
    $ speak(NICOLE, "Oh you don't believe me?")
    $ setWait(22.987,28.284)
    $ speak(LYNN, "Your friend Jessica here was there too and also seems quite surprised at your claim.")
    $ setWait(28.284,31.621)
    $ speak(NICOLE, "Well she's just in shock from years of abuse, right?")
    show jecka sc4 unhappy:
        xzoom -1
    $ setWait(31.621,32.705)
    $ speak(JECKA, "You could call it that.")
    $ setWait(32.705,41.631)
    $ speak(LYNN, "Uh uh, I see what's going on here. Just because I'm an openly feminist woman in power doesn't mean I'll believe any girl who walks in with a last minute accusation.")
    show nicole sc6 angry:
        leftstage
    $ setWait(41.631,47.428)
    $ speak(NICOLE, "Well I guess you're just a non-feminist woman in power cause I'm catching R's left and right from this fuckin' guy and you don't even believe me.")
    $ setWait(47.428,53.101)
    $ speak(LYNN, "Oh, would you like me to call your parents then? It's so serious they should know too, don't you agree?")
    show jecka sc4 surprised:
        xalign .3
    $ setWait(53.101,54.018)
    $ speak(JECKA, "Oh my god.")
    $ setWait(54.018,56.437)
    $ speak(NICOLE, "Uh.. y'know yeah do it.")
    show lynn:
        rightcenterstage
        xzoom -1
        linear 2.7 off_right
    $ setWait(56.437,59.065)
    $ speak(LYNN, "I'll be in the back room then.")
    show jecka sc4 angry:
        xzoom 1
    $ setWait(59.065,60.233)
    $ speak(JECKA, "What are you doing?")
    hide lynn
    $ setWait(60.233,61.442)
    $ speak(NICOLE, "Not getting in trouble.")
    $ setWait(61.442,65.238)
    $ speak(JECKA, "What if she calls my parents too over this shit? I don't wanna deal with this, Nicole.")
    $ setWait(65.238,68.032)
    $ speak(NICOLE, "Relax I'll just tell everyone he threatened to kill you if you squealed.")
    $ setWait(68.032,70.076)
    $ speak(JECKA, "This isn't Julliard, I can't fake that!")
    $ setWait(70.076,73.496)
    $ speak(NICOLE, "Look she probably won't even call yours anyway, don't freak out over it.")
    $ setWait(73.496,74.747)
    $ speak(JECKA, "Let's hope you're right.")
    stop ambient fadeout 4.5
    show black:
        alpha 0.0
        pause 2.8
        linear 2 alpha 1.0
    $ setWait(74.747,80.708)
    $ speak(NICOLE, "I'll take it to court if I have to.")
    jump scene_0138
label scene_0138:
    $ setVoiceTrack("audio/Scenes/0138.mp3")
    play ambient "audio/Ambience/Neighborhood_Ambience_Night.mp3" fadein 1.2
    scene onlayer master
    show black
    show home nicole ext night with Pause(2.96):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.96 zoom .6 truecenter

    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3"
    show nicole sc6:
        centerstage

    show mom 5:
        off_left
        xzoom -1
        linear 1.75 leftstage
    $ setWait(2.96,9.008)
    $ speak(MOM, "Nicole, why was your principal on the phone telling me you may or may not have been sexually assaulted?")
    show nicole sc6:
        xzoom -1
    $ setWait(9.008,13.304)
    $ speak(NICOLE, "Oh that. Uh, it was probably just an April fools prank.")
    $ setWait(13.304,14.805)
    $ speak(MOM, "It's October.")
    $ setWait(14.805,22.396)
    $ speak(NICOLE, "No yeah I know that, it's actually school pride week where we just do the holidays all fucky. Thursday's Rosh Hashanah, could I pass for Jewish?")
    $ setWait(22.396,24.315)
    $ speak(MOM, "What bush are you beating around here?")
    $ setWait(24.315,31.197)
    $ speak(NICOLE, "Okay fine, my Photography teacher was getting really touchy feely with uh...")
    show mom 5 concerned:
        leftstage
        linear 0.45 xalign 0.16
    $ setWait(31.197,34.2)
    $ speak(MOM, "Touchy feely where? Where did he touch you?")
    $ setWait(34.2,35.993)
    $ speak(NICOLE, "My essential areas.")
    $ setWait(35.993,39.538)
    $ speak(MOM, "Are you being serious with me? If not you're in big trouble.")
    show nicole sc6 sad:
        xzoom -1
        centerstage
    $ setWait(39.538,45.044)
    $ speak(NICOLE, "Well in the case-- Mom! I wouldn't joke about this. His fingers were like in.")
    $ setWait(45.044,46.67)
    $ speak(MOM, "...I believe you sweetheart.")
    show nicole sc6 smile:
        xzoom -1
        centerstage
    $ setWait(46.67,49.34)
    $ speak(NICOLE, "Oh awesome, you rock, Mom. So what's for dinner--")
    show nicole sc6:
        xzoom -1
        centerstage

    show mom 5 angry:
        xalign 0.16
    $ setWait(49.34,58.182)
    $ speak(MOM, "But if this really happened I'm not very fond of your principal's dismissive tone. I never thought we'd have to do this at a school so nice, but I'm calling a lawyer.")
    menu:
        "DOUBLE DOWN":
            jump scene_0139
        "DON'T FEEL LIKE GETTING ROPED IN":
            jump scene_0140
label scene_0139:
    $ setVoiceTrack("audio/Scenes/0139.mp3")
    scene home nicole int
    show nicole sc6 surprised:
        xzoom -1
        centerstage

    show mom 5:
        xzoom -1
        xalign 0.16
    $ setWait(0.210,3.795)
    $ speak(NICOLE, "No way. You're actually gonna do something about it? Aren't we broke?")
    $ setWait(3.795,7.715)
    $ speak(MOM, "Oh I just tell you that so you never ask me to buy you things, this is serious.")
    show nicole sc6:
        xzoom -1
        centerstage
    $ setWait(7.715,9.968)
    $ speak(NICOLE, "Wow. I mean-- you know good lawyers?")
    $ setWait(9.968,13.012)
    $ speak(MOM, "I've been married 8 times, I'm well connected.")
    $ setWait(13.012,17.141)
    $ speak(NICOLE, "Well good let's pin Mr. White and his child molesting ways.")
    $ setWait(17.141,23.189)
    $ speak(MOM, "How exactly does he even.. isolate you? There's so many people there as it is.")
    $ setWait(23.189,25.441)
    $ speak(NICOLE, "Isolate? I don't get it.")
    $ setWait(25.441,31.114)
    $ speak(MOM, "Well he has to get you girls alone somehow to... have his way.")
    $ setWait(31.114,35.159)
    $ speak(NICOLE, "Oh yeah um, yeah no he just does it right in the middle of class.")
    $ setWait(35.159,36.077)
    $ speak(MOM, "You're joking.")
    $ setWait(36.077,39.956)
    $ speak(NICOLE, "Yeah just grabbing titties with no shame, he threatens to kill us if we tell anyone.")
    show mom 5 angry:
        xzoom -1
        xalign 0.16
    $ setWait(39.956,42.083)
    $ speak(MOM, "That is un-fucking-believable.")
    $ setWait(42.083,45.628)
    $ speak(NICOLE, "I know. There's like 29 of us so that's a whole lot of killing.")
    $ setWait(45.628,52.176)
    $ speak(MOM, "Y'know what? I'm just seeing red right now-- I will spare no expense to make sure this pervert's under the jail.")
    stop ambient fadeout 2
    jump scene_0141
label scene_0140:
    $ setVoiceTrack("audio/Scenes/0140.mp3")
    scene home nicole int
    show nicole sc6 sad:
        xzoom -1
        centerstage

    show mom 5 concerned:
        xzoom -1
        xalign 0.16
    $ setWait(0.046,2.715)
    $ speak(NICOLE, "Wait mom, don't.")
    $ setWait(2.715,5.426)
    $ speak(MOM, "Oh god, did he brainwash you into liking it?")
    show nicole sc6:
        xzoom -1
        centerstage
    $ setWait(5.426,8.263)
    $ speak(NICOLE, "Excuse me? Mom no just please don't call.")
    $ setWait(8.263,13.643)
    $ speak(MOM, "It's okay sweetie, when you're in college you'll meet plenty of men with just as much money as your photography teacher.")
    $ setWait(13.643,16.646)
    $ speak(NICOLE, "No ew! I made all the shit up, okay?")
    show mom 5:
        xzoom -1
        xalign 0.16
    $ setWait(16.646,18.648)
    $ speak(MOM, "Oh did you now?")
    show nicole sc6 sad:
        xzoom -1
        centerstage
    $ setWait(18.648,25.822)
    $ speak(NICOLE, "Yeah.. could you not ground me forever? I know pretending to be raped is taboo but it was kind of a dry run for when I'm in college.")
    $ setWait(25.822,31.16)
    $ speak(MOM, "Hm.. I won't ground you at all actually. Hop in the car, let's go to a tattoo place.")
    show nicole sc6 smile:
        xzoom -1
        centerstage
    $ setWait(31.16,37.792)
    $ speak(NICOLE, "Oh my god, Mom are you serious? You know I've wanted one for so long, is this like some kind of reward for being honest?")
    $ setWait(37.792,43.673)
    $ speak(MOM, "Quite the opposite, I had a chat with your friend Jecka's mother at the last parent-teacher conference.")
    show nicole sc6 surprised:
        xzoom -1
        centerstage
    $ setWait(43.673,45.133)
    $ speak(NICOLE, "And what'd she say?")
    $ setWait(45.133,49.095)
    $ speak(MOM, "A lot of words, but 2 in particular really stuck out to me...")
    $ setWait(49.095,51.514)
    $ speak(MOM, "...Disciplinary Tattoo.")
    show nicole sc6 surprised:
        xzoom -1
        centerstage
        linear 2 xalign 0.58
    $ setWait(51.514,54.684)
    $ speak(NICOLE, "Uh.. fill me in on what that is, sounds familiar.")
    $ setWait(54.684,58.521)
    $ speak(MOM, "I'm getting \"Jesus Saves\" tattooed down your spine.")
    show mom 5:
        xalign 0.16
        linear 3.2 off_right

    show nicole sc6 sad:
        xalign 0.58
        pause 1.3
        xalign 0.54
        xzoom 1
        pause 1.4
        linear 2.2 off_right
    $ setWait(58.521,64.652)
    $ speak(NICOLE, "What!? Mom! No! This is fucking weird! Everyone at nice beaches'll laugh at me, and everyone at shitty beaches'll hit on me.")
    stop ambient fadeout 2
    jump scene_0146
label scene_0141:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.6 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0141.mp3")
    play ambient "audio/ambience/courtroom_ambience.mp3" fadein 2
    scene courtroom
    show nicole court:
        leftstage

    show lawyer:
        rightcenterstage
    $ setWait(0.789,8.762)
    $ speak(LAWYER, "So Nicole, in your own words, what happened at school on the day of the 18th?")
    $ setWait(8.762,18.48)
    $ speak(NICOLE, "Yeah okay so, I'm just doing my makeup in class, not bothering anyone or anything and Mr. White had a huge problem with that.")
    $ setWait(18.48,21.233)
    $ speak(LAWYER, "I see. Go on.")
    $ setWait(21.233,29.241)
    $ speak(NICOLE, "His face was totally calm while he proceeded to flip the whole desk over. And it's an art class so the table's huge, big enough for 4 kids.")
    $ setWait(29.241,30.451)
    $ speak(LAWYER, "Really now?")
    $ setWait(30.451,36.123)
    $ speak(NICOLE, "Yeah he grabbed me to a standing position, getting right behind and grinded against me.")
    $ setWait(36.123,41.17)
    $ speak(NICOLE, "In front of all the students too. Then his hand started massaging my breasts it was so--")
    $ setWait(41.17,45.883)
    $ speak(LAWYER, "Wait I'm sorry, one hand on both of them?")
    $ setWait(45.883,47.051)
    $ speak(NICOLE, "Yeah.")
    $ setWait(47.051,50.554)
    $ speak(LAWYER, "I hope the jury notes these logistical inaccuracies.")
    $ setWait(50.554,58.604)
    $ speak(NICOLE, "Well see I'm a tiny 17 year old minor and his man hands were more than big enough to wrap around half my body.")
    $ setWait(58.604,60.981)
    $ speak(LAWYER, "Fine then, continue.")
    $ setWait(60.981,67.988)
    $ speak(NICOLE, "So then he's poking his tongue all over my neck and whispering things I'd.. rather not repeat.")
    $ setWait(67.988,70.491)
    $ speak(LAWYER, "You're under oath now, Nicole.")
    $ setWait(70.491,82.419)
    $ speak(NICOLE, "Huh, well you asked for it. He called me his voluptuous teen property and said my sexual willingness would pull a fine ransom on the black market.")
    show lawyer angry:
        rightcenterstage
    $ setWait(82.419,84.213)
    $ speak(LAWYER, "Alright, alright! Enough of this!")
    $ setWait(84.213,86.006)
    $ speak(KYLAR, "Nah this is hot, keep going!")
    show lawyer:
        rightcenterstage
    $ setWait(86.006,91.929)
    $ speak(LAWYER, "This is quite the imagination you have but... really, people?")
    $ setWait(91.929,104.274)
    $ speak(LAWYER, "Are we going to believe this charade when the school's shown no other evidence of misconduct from it's faculty? You have a lot of explaining to do, we'll wait.")
    menu:
        "RIDE THIS TO THE BANK":
            jump scene_0142
        "AVOID GETTING MURDERED\nAFTER HE'S FIRED":
            jump scene_0143
label scene_0142:
    $ setVoiceTrack("audio/Scenes/0142.mp3")
    scene courtroom
    show nicole court:
        leftstage

    show lawyer:
        rightcenterstage
    $ setWait(0.041,3.753)
    $ speak(NICOLE, "So just cause no one said anything means it isn't happening?")
    $ setWait(3.753,7.84)
    $ speak(LAWYER, "You all have internet and texting now, surely it would've gotten out.")
    $ setWait(7.84,18.225)
    $ speak(NICOLE, "Even if someone did say something, who's better connected? The 16 year old girl who doesn't hang out at the local sports bar? Or some dipshit with a whistle who knows 12 synonyms for Quarterback?")
    $ setWait(18.225,20.352)
    $ speak(LAWYER, "And what's the implication here?")
    $ setWait(20.352,27.193)
    $ speak(NICOLE, "Men listen to other men? Male teachers, male superintendent, male security guards, male everything.")
    $ setWait(27.193,33.491)
    $ speak(LAWYER, "Male everything-- however! ...A female principal?")
    $ setWait(33.491,37.495)
    $ speak(NICOLE, "When you look like Miss Lynn you could be governor, let alone principal.")
    $ setWait(37.495,44.001)
    $ speak(LAWYER, "Are you telling the jury she's only in that position because of the physical favors she can offer as a woman?")
    $ setWait(44.001,49.715)
    $ speak(NICOLE, "No. It's not a woman thing, it's a she's attractive thing. You think ugly bitches get handouts?")
    $ setWait(49.715,54.095)
    $ speak(LAWYER, "Could we please show the jury a faculty headshot of Principal Lynn?")
    $ setWait(54.095,55.93)
    $ speak(NICOLE, "What the fuck does this have to do with anything?")
    $ setWait(55.93,58.307)
    $ speak(LAWYER, "You're in the court of law, please act like it.")
    $ setWait(58.307,68.609)
    $ speak(NICOLE, "You're beating around the bush. The gym teacher's asked me out like 3 times since I've been here and the counselor gives every girl a lecture on normalizing pedophilia.")
    $ setWait(68.609,70.903)
    $ speak(LAWYER, "Now surely you don't believe this!")
    $ setWait(70.903,74.115)
    $ speak(NICOLE, "Oh let me read the last few texts from Coach Colby then.")
    $ setWait(74.115,81.914)
    $ speak(NICOLE, "\"Hey sexy you up\" \"How deep is your throat\" \"I wanna murder my wife and shower you in the life insurance payout\"")
    $ setWait(81.914,87.086)
    $ speak(NICOLE, "And they still have this guy? Why is he able to be on the payroll?")
    show lawyer:
        xzoom -1
    $ setWait(87.086,93.175)
    $ speak(LAWYER, "Settle down! Mister Colby was fired and incarcerated months ago promptly after a few reports!")
    $ setWait(93.175,96.887)
    $ speak(NICOLE, "You just said no one ever reported anything like 5 minutes ago.")
    show lawyer angry:
        xzoom 1
    $ setWait(96.887,100.099)
    $ speak(LAWYER, "Dammit!")
    show text colby
    $ setWait(100.099,102.268)
    $ speak(NICOLE, "Oh coach just texted me again.")
    show lawyer:
        xzoom 1
    hide text colby
    $ setWait(102.268,113.028)
    $ speak(NICOLE, "\"Hey honey just got out of jail, good news they're giving me my job back so we can still hang out\"")
    show lawyer:
        rightcenterstage
        pause 1.7
        linear 2.2 leftcenterstage
    $ setWait(113.028,117.533)
    $ speak(LAWYER, "Nicole, you've been my hardest cross examination yet.")
    show black:
        alpha 0.0
        pause 3.5
        linear 4.5 alpha 1.0
    stop ambient fadeout 6.5
    $ setWait(117.533,126.501)
    $ speak(NICOLE, "Oh, well you've just been a bitch in general. Go iron your Mickey Mouse tie.")
    jump end_0144
label scene_0143:
    $ setVoiceTrack("audio/Scenes/0143.mp3")
    scene courtroom
    show nicole court:
        leftstage

    show lawyer:
        rightcenterstage
    $ setWait(0.046,3.174)
    $ speak(NICOLE, "I mean, I already explained it, didn't I?")
    $ setWait(3.174,10.181)
    $ speak(LAWYER, "You know what I mean, why isn't the rest of the faculty testifying in your favor? Any further details?")
    show nicole court sad:
        leftstage
    $ setWait(10.181,13.392)
    $ speak(NICOLE, "Uh, the whole thing was kind of fuzzy.")
    show lawyer angry:
        rightcenterstage
        linear 4 leftcenterstage
    $ setWait(13.392,17.939)
    $ speak(LAWYER, "Fuzzy? Or abstract. Fictional. Made up.")
    show nicole court scream:
        leftstage
    $ setWait(17.939,19.023)
    $ speak(NICOLE, "Alright!")
    $ setWait(19.023,21.275)
    $ speak(LAWYER, "Alright what?")
    show nicole court sad:
        leftstage
    $ setWait(21.275,24.779)
    $ speak(NICOLE, "...I made it up, the whole thing.")
    show lawyer:
        leftcenterstage
        xzoom -1
        linear 2.8 rightcenterstage
    $ setWait(24.779,27.531)
    $ speak(LAWYER, "I knew you'd crack eventually.")
    $ setWait(27.531,33.454)
    $ speak(NICOLE, "But how can you blame me? Just trying to put on my makeup and he belittles me in front of the whole class.")
    $ setWait(33.454,39.46)
    $ speak(NICOLE, "You'd want to get even if you were in my position too. It's hard being me, can anyone understand that?")
    show black:
        alpha 0.0
        pause 3.5
        linear 2.5 alpha 1.0
    stop ambient fadeout 6.5
    $ setWait(39.46,46.841)
    $ speak(LAWYER, "I understand this case is over.")
    jump end_0145

label end_0144:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0144" not in persistent.endings:
        $ persistent.endings.append("end_0144")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0144end with Pause (24.8):
        alpha 1.0
    return

label end_0145:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0145" not in persistent.endings:
        $ persistent.endings.append("end_0145")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0145end with Pause (29.7):
        alpha 1.0
    return

label scene_0146:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.6 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0146.mp3")
    scene cafeteria int 2
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1.5
    show nicole sc7:
        leftcenterstage
    show jecka sc5 unhappy:
        rightcenterstage
    $ setWait(0.044,2.546)
    $ speak(NICOLE, "...So fuck photography.")
    $ setWait(2.546,3.672)
    $ speak(JECKA, "Yeah pretty much.")
    show nicole sc7 angry:
        leftcenterstage
    $ setWait(3.672,10.888)
    $ speak(NICOLE, "Mr. White acts like his class is so god damn important. We can take pictures with a camera phone, who even needs a camera camera anymore?")
    show jecka sc5 angry:
        rightcenterstage
    $ setWait(10.888,16.685)
    $ speak(JECKA, "Exactly. Men who teach electives get so insecure when they realize they can't stop anyone from graduating.")
    $ setWait(16.685,18.979)
    $ speak(NICOLE, "Bitch be happy anyone even took your class.")
    $ setWait(18.979,22.691)
    $ speak(JECKA, "It's an art course anyway, like doing your makeup's a huge step down.")
    show kylar sc3:
        off_right
        linear 0.85 rightstage

    show jecka sc5 unhappy:
        pause 0.6
        xzoom -1
    $ setWait(22.691,24.234)
    $ speak(KYLAR, "What's up you whores?")
    show nicole sc7:
        leftcenterstage
    $ setWait(24.234,25.194)
    $ speak(NICOLE, "Wow.")
    $ setWait(25.194,26.612)
    $ speak(JECKA, "Hi Kylar..")
    $ setWait(26.612,30.282)
    $ speak(KYLAR, "You shit talking Mr. White? Yeah he probably deserves it.")
    $ setWait(30.282,31.241)
    $ speak(NICOLE, "What do you want?")
    show kylar sc3 unhappy:
        rightstage
    $ setWait(31.241,34.953)
    $ speak(KYLAR, "Alright damn, did you guys get an invite to Kelly's pool party?")
    $ setWait(34.953,35.913)
    $ speak(NICOLE, "It's October.")
    show jecka sc5 unhappy:
        xzoom 1
    $ setWait(35.913,38.665)
    $ speak(JECKA, "No her parents are like really rich it's glassed in and everything.")
    show jecka sc5 unhappy:
        pause 1
        xzoom -1

    show kylar sc3:
        rightstage
    $ setWait(38.665,43.837)
    $ speak(KYLAR, "Yeah and her pool stuff is sick, they got those 4 foot long syringe water gun things.")
    $ setWait(43.837,44.797)
    $ speak(NICOLE, "What're you 10?")
    $ setWait(44.797,48.175)
    $ speak(KYLAR, "Whatever just a little fun on the side while picking up bitches.")
    $ setWait(48.175,51.72)
    $ speak(NICOLE, "I've been here for a year and never once heard of someone having sex with you.")
    $ setWait(51.72,53.931)
    $ speak(JECKA, "I've been here since 3rd grade and haven't heard it.")
    show kylar sc3 unhappy:
        rightstage
    $ setWait(53.931,56.725)
    $ speak(KYLAR, "Nuh-uh, remember freshman year with Jenny Fillmore?")
    show jecka sc5 angry:
        xzoom -1
        rightcenterstage
    $ setWait(56.725,59.728)
    $ speak(JECKA, "She was unconscious how do you still brag about that!?")
    $ setWait(59.728,61.73)
    $ speak(NICOLE, "You're like the reason they have women's college.")
    $ setWait(61.73,64.525)
    $ speak(KYLAR, "Okay old news whatever-- you have invites or not?")
    show jecka sc5 unhappy:
        xzoom -1
        rightcenterstage
    $ setWait(64.525,65.025)
    $ speak(JECKA, "Yeah.")
    $ setWait(65.025,65.818)
    $ speak(NICOLE, "Me too.")
    $ setWait(65.818,68.445)
    $ speak(KYLAR, "How did you get one, you haven't even been here that long.")
    $ setWait(68.445,70.989)
    $ speak(NICOLE, "Cause I have a nice face and I'm not fat?")
    $ setWait(70.989,76.286)
    $ speak(KYLAR, "Okay well can I tag along with you guys? This weekend's gonna be so boring if I can't go.")
    $ setWait(76.286,84.002)
    $ speak(JECKA, "I don't wanna be responsible for you ruining the party, but I also don't wanna be responsible for you crashing it out of roid rage. Nicole's choice.")
    $ setWait(84.002,90.425)
    $ speak(KYLAR, "Fine. Nicole, I know I called you a whore like 2 minutes ago but you could let me go with you just this once?")
    menu:
        "WE DON'T HANG OUT\nWITH RAPISTS":
            jump scene_0147
        "ON ONE CONDITION":
            jump scene_0148
label scene_0147:
    $ setVoiceTrack("audio/Scenes/0147.mp3")
    scene cafeteria int 2
    show kylar sc3 unhappy:
        rightstage

    show jecka sc5 unhappy:
        rightcenterstage
        xzoom -1

    show nicole sc7 angry:
        leftcenterstage

    $ setWait(0.038,1.456)
    $ speak(NICOLE, "No, fuck off!")
    show kylar sc3:
        rightstage
        pause 1.7
        xzoom -1
        linear 1.6 off_right
    $ setWait(1.456,3.75)
    $ speak(KYLAR, "Fine be a bitch, see if I care.")
    show jecka sc5:
        rightcenterstage
        xzoom -1
    $ setWait(3.75,6.919)
    $ speak(JECKA, "You're just mad you can't see us in bikinis this weekend!")
    hide kylar
    $ setWait(6.919,8.004)
    $ speak(NICOLE, "What're you doing!?")
    show jecka sc5 unhappy:
        xzoom 1
    $ setWait(8.004,8.463)
    $ speak(JECKA, "What?")
    $ setWait(8.463,13.384)
    $ speak(NICOLE, "Don't get him flustered like that. He's a rapist, sex turns into violence overnight for those types.")
    $ setWait(13.384,14.927)
    $ speak(JECKA, "What like choking and biting?")
    $ setWait(14.927,21.434)
    $ speak(NICOLE, "That and jerking off while thinking about us suddenly turning into \"Jecka would look so hot with her organs gouged out\".")
    $ setWait(21.434,22.894)
    $ speak(JECKA, "...How do you know these things?")
    show nicole sc7:
        leftcenterstage
    $ setWait(22.894,24.687)
    $ speak(NICOLE, "I had a brother.")
    stop ambient fadeout 2
    jump scene_0149A
label scene_0148:
    $ setVoiceTrack("audio/Scenes/0148.mp3")
    scene cafeteria int 2
    show kylar sc3 unhappy:
        rightstage

    show jecka sc5 unhappy:
        rightcenterstage
        xzoom -1

    show nicole sc7:
        leftcenterstage

    $ setWait(0.043,6.132)
    $ speak(NICOLE, "Uh maybe, but you need a conversation starter if we're gonna justify bringing you.")
    $ setWait(6.132,6.966)
    $ speak(KYLAR, "Like what?")
    $ setWait(6.966,11.596)
    $ speak(NICOLE, "Do something impressive this week like.. like..")
    show jecka sc5:
        rightcenterstage
        xzoom -1
    $ setWait(11.596,13.723)
    $ speak(JECKA, "Like put something funny on YouTube.")
    $ setWait(13.723,17.644)
    $ speak(NICOLE, "Yeah actually not a bad idea, then everybody can watch it at the party.")
    $ setWait(17.644,19.437)
    $ speak(KYLAR, "A video of what though?")
    $ setWait(19.437,21.272)
    $ speak(NICOLE, "You know where photography is?")
    $ setWait(21.272,23.149)
    $ speak(KYLAR, "At magazine studios, duh.")
    show nicole sc7 angry:
        leftcenterstage
    $ setWait(23.149,25.652)
    $ speak(NICOLE, "No dipshit-- the photography classroom.")
    $ setWait(25.652,27.028)
    $ speak(KYLAR, "Yeah what about it?")
    show nicole sc7:
        leftcenterstage
    $ setWait(27.028,33.576)
    $ speak(NICOLE, "The dark room has a whole bunch of really delicate and expensive equipment, make a video of you just destroying that shit.")
    $ setWait(33.576,35.828)
    $ speak(KYLAR, "Huh, really? What do you think, Jecka?")
    $ setWait(35.828,39.749)
    $ speak(JECKA, "I think Mr. White's reaction would be funnier than the video itself so go for it.")
    show kylar sc3:
        pause 3.2
        rightstage
        xzoom -1
        linear 2 off_right
    $ setWait(39.749,45.63)
    $ speak(KYLAR, "Fine, you're on. See you there this weekend. Heh yeah makin' friends.")
    hide kylar
    show jecka sc5 unhappy:
        rightcenterstage
        xzoom 1
    $ setWait(45.63,49.425)
    $ speak(JECKA, "It's amazing how men will do anything just to see us with less clothes on.")
    $ setWait(49.425,52.162)
    $ speak(NICOLE, "Yeah it's like there's laws for it or something.")
    stop ambient fadeout 2
    jump scene_0149B
label scene_0149A:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.6 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0149.mp3")
    scene school ext 3
    play ambient "audio/ambience/school_ext_ambience.mp3" fadein 1.4
    show girl_4 color2:
        rightcenterstage

    show girl_2 unhappy:
        leftcenterstage
        xzoom -1

    $ setWait(0.251,3.17)
    $ speak(GIRL_2, "So what're you wearing to Kelly's pool party?")
    $ setWait(3.17,5.631)
    $ speak(GIRL_4, "Well Summer's over so nowhere's selling anything.")
    show couns 3 smile:
        off_right
        linear 1.2 rightstage

    show girl_4 color2:
        pause 0.6
        xzoom -1
        linear 0.25 xalign 0.63
    $ setWait(5.631,10.136)
    $ speak(COUNSELOR, "Hello, girls. Going to a pool party in the fall?")
    $ setWait(10.136,14.181)
    $ speak(GIRL_4, "Yeah, well I don't know maybe. I can't find anything to wear for it.")
    $ setWait(14.181,15.933)
    $ speak(COUNSELOR, "I could help you out with that.")
    $ setWait(15.933,17.184)
    $ speak(GIRL_2, "You sell bikinis?")
    $ setWait(17.184,26.652)
    $ speak(COUNSELOR, "Of course not, but swing by my office later and we could take some measurements for the home ec sewing club. We'll make sure it fits flawlessly to your every curve.")
    $ setWait(26.652,29.572)
    $ speak(GIRL_4, "Gee thanks, I'll see ya there maybe.")
    show couns 3 smile:
        xzoom -1
        rightstage
        linear 1.8 off_right
    $ setWait(29.572,32.575)
    $ speak(COUNSELOR, "Have a good day at school.")
    $ setWait(32.575,35.453)
    $ speak(GIRL_2, "Did he just say \"your every curve\"?")
    show girl_4 color2:
        xzoom 1
    $ setWait(35.453,37.538)
    $ speak(GIRL_4, "Yeah is he allowed to say that??")
    show nicole sc5:
        off_left
        linear 1.5 leftstage

    show girl_2 unhappy:
        pause 0.65
        xzoom 1
    $ setWait(37.538,39.248)
    $ speak(NICOLE, "What are you guys freaking out about?")
    $ setWait(39.248,42.501)
    $ speak(GIRL_4, "I think the counselor might've made an advance at me?")
    show girl_2 unhappy:
        xzoom -1
    $ setWait(42.501,46.005)
    $ speak(GIRL_2, "He literally asked you to go to his office, get naked, and be measured.")
    $ setWait(46.005,47.715)
    $ speak(NICOLE, "Yawn, what else is new?")
    $ setWait(47.715,48.466)
    $ speak(GIRL_4, "What?")
    $ setWait(48.466,51.635)
    $ speak(NICOLE, "You've gone here longer than me, how did you not notice?")
    show girl_2 unhappy:
        xzoom 1
    $ setWait(51.635,53.262)
    $ speak(GIRL_2, "To be fair he's kinda subtle about it.")
    $ setWait(53.262,56.307)
    $ speak(NICOLE, "He's what I call a marathon pedophile.")
    $ setWait(56.307,59.81)
    $ speak(GIRL_4, "Sorry but, what the fuck is a \"marathon pedophile\"?")
    $ setWait(59.81,67.568)
    $ speak(NICOLE, "He tries to make you question society's hatred of pedophilia before he actually molests you. Then you'll feel bad if you tell on him afterward.")
    $ setWait(67.568,70.654)
    $ speak(GIRL_2, "So he guilts you so he can make a routine out of it?")
    $ setWait(70.654,75.034)
    $ speak(NICOLE, "Exactly, a predator that plays the long-game. A marathon pedophile.")
    $ setWait(75.034,78.245)
    $ speak(GIRL_4, "That's like 3 levels worse than what I thought he was gonna do.")
    $ setWait(78.245,80.081)
    $ speak(NICOLE, "Why did he even wanna measure you anyway?")
    $ setWait(80.081,83.584)
    $ speak(GIRL_4, "For a bikini to wear at Kelly's pool party. He'd have home ec make it.")
    show nicole sc5 angry:
        leftstage
    $ setWait(83.584,86.67)
    $ speak(NICOLE, "Home ec? What're they gonna make? A fucking felt bathing suit?")
    $ setWait(86.67,91.634)
    $ speak(GIRL_4, "I didn't say I was gonna do it! But yeah it'd probably fall apart after a lap in the pool anyway.")
    show girl_2:
        xzoom -1
    show nicole sc5:
        leftstage
    $ setWait(91.634,94.929)
    $ speak(GIRL_2, "Excuse me? You planned on swimming at a pool party?")
    $ setWait(94.929,96.639)
    $ speak(GIRL_4, "What do you do at a pool party?")
    $ setWait(96.639,97.807)
    $ speak(GIRL_2, "Sit around and look cute.")
    $ setWait(97.807,99.158)
    $ speak(NICOLE, "Same.")
    stop ambient fadeout 2
    jump scene_0150A
label scene_0149B:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.6 alpha 0.0
    play ambient "audio/ambience/school_ext_ambience.mp3" fadein 1.4
    $ setVoiceTrack("audio/Scenes/0149.mp3")
    scene school ext 3
    show girl_4 color2:
        rightcenterstage

    show girl_2 unhappy:
        leftcenterstage
        xzoom -1

    $ setWait(0.251,3.17)
    $ speak(GIRL_2, "So what're you wearing to Kelly's pool party?")
    $ setWait(3.17,5.631)
    $ speak(GIRL_4, "Well Summer's over so nowhere's selling anything.")
    show couns 3 smile:
        off_right
        linear 1.2 rightstage

    show girl_4 color2:
        pause 0.6
        xzoom -1
        linear 0.25 xalign 0.63
    $ setWait(5.631,10.136)
    $ speak(COUNSELOR, "Hello, girls. Going to a pool party in the fall?")
    $ setWait(10.136,14.181)
    $ speak(GIRL_4, "Yeah, well I don't know maybe. I can't find anything to wear for it.")
    $ setWait(14.181,15.933)
    $ speak(COUNSELOR, "I could help you out with that.")
    $ setWait(15.933,17.184)
    $ speak(GIRL_2, "You sell bikinis?")
    $ setWait(17.184,26.652)
    $ speak(COUNSELOR, "Of course not, but swing by my office later and we could take some measurements for the home ec sewing club. We'll make sure it fits flawlessly to your every curve.")
    $ setWait(26.652,29.572)
    $ speak(GIRL_4, "Gee thanks, I'll see ya there maybe.")
    show couns 3 smile:
        xzoom -1
        rightstage
        linear 1.8 off_right
    $ setWait(29.572,32.575)
    $ speak(COUNSELOR, "Have a good day at school.")
    $ setWait(32.575,35.453)
    $ speak(GIRL_2, "Did he just say \"your every curve\"?")
    show girl_4 color2:
        xzoom 1
    $ setWait(35.453,37.538)
    $ speak(GIRL_4, "Yeah is he allowed to say that??")
    show nicole sc5:
        off_left
        linear 1.5 leftstage

    show girl_2 unhappy:
        pause 0.65
        xzoom 1
    $ setWait(37.538,39.248)
    $ speak(NICOLE, "What are you guys freaking out about?")
    $ setWait(39.248,42.501)
    $ speak(GIRL_4, "I think the counselor might've made an advance at me?")
    show girl_2 unhappy:
        xzoom -1
    $ setWait(42.501,46.005)
    $ speak(GIRL_2, "He literally asked you to go to his office, get naked, and be measured.")
    $ setWait(46.005,47.715)
    $ speak(NICOLE, "Yawn, what else is new?")
    $ setWait(47.715,48.466)
    $ speak(GIRL_4, "What?")
    $ setWait(48.466,51.635)
    $ speak(NICOLE, "You've gone here longer than me, how did you not notice?")
    show girl_2 unhappy:
        xzoom 1
    $ setWait(51.635,53.262)
    $ speak(GIRL_2, "To be fair he's kinda subtle about it.")
    $ setWait(53.262,56.307)
    $ speak(NICOLE, "He's what I call a marathon pedophile.")
    $ setWait(56.307,59.81)
    $ speak(GIRL_4, "Sorry but, what the fuck is a \"marathon pedophile\"?")
    $ setWait(59.81,67.568)
    $ speak(NICOLE, "He tries to make you question society's hatred of pedophilia before he actually molests you. Then you'll feel bad if you tell on him afterward.")
    $ setWait(67.568,70.654)
    $ speak(GIRL_2, "So he guilts you so he can make a routine out of it?")
    $ setWait(70.654,75.034)
    $ speak(NICOLE, "Exactly, a predator that plays the long-game. A marathon pedophile.")
    $ setWait(75.034,78.245)
    $ speak(GIRL_4, "That's like 3 levels worse than what I thought he was gonna do.")
    $ setWait(78.245,80.081)
    $ speak(NICOLE, "Why did he even wanna measure you anyway?")
    $ setWait(80.081,83.584)
    $ speak(GIRL_4, "For a bikini to wear at Kelly's pool party. He'd have home ec make it.")
    show nicole sc5 angry:
        leftstage
    $ setWait(83.584,86.67)
    $ speak(NICOLE, "Home ec? What're they gonna make? A fucking felt bathing suit?")
    $ setWait(86.67,91.634)
    $ speak(GIRL_4, "I didn't say I was gonna do it! But yeah it'd probably fall apart after a lap in the pool anyway.")
    show girl_2:
        xzoom -1
    show nicole sc5:
        leftstage
    $ setWait(91.634,94.929)
    $ speak(GIRL_2, "Excuse me? You planned on swimming at a pool party?")
    $ setWait(94.929,96.639)
    $ speak(GIRL_4, "What do you do at a pool party?")
    $ setWait(96.639,97.807)
    $ speak(GIRL_2, "Sit around and look cute.")
    $ setWait(97.807,99.158)
    $ speak(NICOLE, "Same.")
    stop ambient fadeout 2
    jump scene_0150B
label scene_0150A:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.6 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0150.mp3")
    scene locker room
    play ambient "audio/ambience/Bathroom_Lockerroom_ambience.mp3" fadein 1.5
    show nicole underwear angry:
        xalign 0.1

    show girl_5 gym:
        xzoom -1
        rightstage
    $ setWait(0.328,6.084)
    $ speak(NICOLE, "God dammit! Why are they still using combination locks? This school's soft, no one steals shit anyway.")
    show girl_5 gym:
        xzoom 1
        rightstage
        linear 1 xalign 0.55
    $ setWait(6.084,7.419)
    $ speak(GIRL_5, "You still aren't dressed?")
    $ setWait(7.419,11.923)
    $ speak(NICOLE, "Yeah they need thumb print scanners or some shit. It's 2008, isn't it the future by now?")
    show girl_5 gym:
        xalign 0.55
        linear 2.5 off_left
    $ setWait(11.923,13.383)
    $ speak(GIRL_5, "You're gonna be late.")
    show flash:
        alpha 0
        pause 2.85
        linear 0.02 alpha 1
        linear 0.2 alpha 0
    $ setWait(13.383,16.72)
    $ speak(NICOLE, "No shit. Now how many spins again?")
    show jeffery camera:
        off_right
        linear 0.5 rightstage
    $ setWait(16.72,17.429)
    $ speak(JEFFERY, "Nailed it!")
    show nicole underwear surprised:
        xalign .1
    $ setWait(17.429,19.389)
    $ speak(NICOLE, "What the fuck! How'd you get in here!?")
    $ setWait(19.389,25.479)
    $ speak(JEFFERY, "There's no lock on the doors. Saw it as a great opportunity for an A+ in Street Photography.")
    show nicole underwear angry:
        xalign .1
    $ setWait(25.479,27.272)
    $ speak(NICOLE, "Did your cartoons tell you to do this?")
    $ setWait(27.272,28.69)
    $ speak(JEFFERY, "Ahem-- Anime!")
    $ setWait(28.69,32.527)
    $ speak(NICOLE, "Why didn't anime tell you to screenshot a cam girl in public or something?")
    show jeffery camera:
        rightstage
        pause 1.62
        linear 4 rightcenterstage
    $ setWait(32.527,38.492)
    $ speak(JEFFERY, "Oh Nicole, if your brain was as big as your ample breasts then maybe you'd understand.")
    $ setWait(38.492,43.663)
    $ speak(NICOLE, "I'm sorry-- do you think you're cool right now? You're a freak, not even the sex fiend counselor wants to fuck you.")
    $ setWait(43.663,48.794)
    $ speak(JEFFERY, "Your petty insults will make the development on this photograph all the more satisfying.")
    $ setWait(48.794,62.182)
    $ speak(JEFFERY, "Cam girls are all cheap digital nonsense, I've captured your succulent figure on medium format film! Every little shadow and highlight of your tantalizing midriff captured the way it was meant to be.")
    $ setWait(62.182,66.394)
    $ speak(NICOLE, "If you're gonna sexually harass me could you not talk like a cartoon character while you do it?")
    $ setWait(66.394,71.65)
    $ speak(JEFFERY, "I do what I want with my words, I'll also do as I please with this photo.")
    show nicole underwear sad:
        xalign .1
    $ setWait(71.65,73.568)
    $ speak(NICOLE, "No come on-- just throw the film out!")
    $ setWait(73.568,79.741)
    $ speak(JEFFERY, "I'm afraid I can't do that. Every boy with a crush on you should pay top dollar for these prints.")
    $ setWait(79.741,86.832)
    $ speak(JEFFERY, "Or maybe I could hang a giant poster of it out front, humiliating you the way you've humiliated me time after time.")
    show nicole underwear angry:
        xalign .1
    $ setWait(86.832,91.878)
    $ speak(NICOLE, "What? Cause I called you a future pedophile in chemistry last year? Kay sorry, now throw it out.")
    show jeffery camera:
        xzoom -1
        rightcenterstage
        linear 0.6 off_right
    $ setWait(91.878,94.84)
    $ speak(JEFFERY, "You won't convince me otherwise!")
    show nicole underwear:
        xalign .1
    $ setWait(94.84,96.591)
    $ speak(NICOLE, "Huh...")
    stop ambient fadeout 4
    show black:
        alpha 0.0
        pause 2
        linear 2 alpha 1.0

    show nicole underwear surprised:
        xalign .1
    $ setWait(96.591,101.436)
    $ speak(NICOLE, "...Wait was I at the wrong locker?")
    jump scene_0151
label scene_0150B:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.6 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0150.mp3")
    scene locker room
    play ambient "audio/ambience/Bathroom_Lockerroom_ambience.mp3" fadein 1.5
    show nicole underwear angry:
        xalign 0.1

    show girl_5 gym:
        xzoom -1
        rightstage
    $ setWait(0.328,6.084)
    $ speak(NICOLE, "God dammit! Why are they still using combination locks? This school's soft, no one steals shit anyway.")
    show girl_5 gym:
        xzoom 1
        rightstage
        linear 1 xalign 0.55
    $ setWait(6.084,7.419)
    $ speak(GIRL_5, "You still aren't dressed?")
    $ setWait(7.419,11.923)
    $ speak(NICOLE, "Yeah they need thumb print scanners or some shit. It's 2008, isn't it the future by now?")
    show girl_5 gym:
        xalign 0.55
        linear 2.5 off_left
    $ setWait(11.923,13.383)
    $ speak(GIRL_5, "You're gonna be late.")
    show flash:
        alpha 0
        pause 2.85
        linear 0.02 alpha 1
        linear 0.2 alpha 0
    $ setWait(13.383,16.72)
    $ speak(NICOLE, "No shit. Now how many spins again?")
    show jeffery camera:
        off_right
        linear 0.5 rightstage
    $ setWait(16.72,17.429)
    $ speak(JEFFERY, "Nailed it!")
    show nicole underwear surprised:
        xalign .1
    $ setWait(17.429,19.389)
    $ speak(NICOLE, "What the fuck! How'd you get in here!?")
    $ setWait(19.389,25.479)
    $ speak(JEFFERY, "There's no lock on the doors. Saw it as a great opportunity for an A+ in Street Photography.")
    show nicole underwear angry:
        xalign .1
    $ setWait(25.479,27.272)
    $ speak(NICOLE, "Did your cartoons tell you to do this?")
    $ setWait(27.272,28.69)
    $ speak(JEFFERY, "Ahem-- Anime!")
    $ setWait(28.69,32.527)
    $ speak(NICOLE, "Why didn't anime tell you to screenshot a cam girl in public or something?")
    show jeffery camera:
        rightstage
        pause 1.62
        linear 4 rightcenterstage
    $ setWait(32.527,38.492)
    $ speak(JEFFERY, "Oh Nicole, if your brain was as big as your ample breasts then maybe you'd understand.")
    $ setWait(38.492,43.663)
    $ speak(NICOLE, "I'm sorry-- do you think you're cool right now? You're a freak, not even the sex fiend counselor wants to fuck you.")
    $ setWait(43.663,48.794)
    $ speak(JEFFERY, "Your petty insults will make the development on this photograph all the more satisfying.")
    $ setWait(48.794,62.182)
    $ speak(JEFFERY, "Cam girls are all cheap digital nonsense, I've captured your succulent figure on medium format film! Every little shadow and highlight of your tantalizing midriff captured the way it was meant to be.")
    $ setWait(62.182,66.394)
    $ speak(NICOLE, "If you're gonna sexually harass me could you not talk like a cartoon character while you do it?")
    $ setWait(66.394,71.65)
    $ speak(JEFFERY, "I do what I want with my words, I'll also do as I please with this photo.")
    show nicole underwear sad:
        xalign .1
    $ setWait(71.65,73.568)
    $ speak(NICOLE, "No come on-- just throw the film out!")
    $ setWait(73.568,79.741)
    $ speak(JEFFERY, "I'm afraid I can't do that. Every boy with a crush on you should pay top dollar for these prints.")
    $ setWait(79.741,86.832)
    $ speak(JEFFERY, "Or maybe I could hang a giant poster of it out front, humiliating you the way you've humiliated me time after time.")
    show nicole underwear angry:
        xalign .1
    $ setWait(86.832,91.878)
    $ speak(NICOLE, "What? Cause I called you a future pedophile in chemistry last year? Kay sorry, now throw it out.")
    show jeffery camera:
        xzoom -1
        rightcenterstage
        linear 0.6 off_right
    $ setWait(91.878,94.84)
    $ speak(JEFFERY, "You won't convince me otherwise!")
    show nicole underwear:
        xalign .1
    $ setWait(94.84,96.591)
    $ speak(NICOLE, "Huh...")
    stop ambient fadeout 4
    show black:
        alpha 0.0
        pause 2
        linear 2 alpha 1.0

    show nicole underwear surprised:
        xalign .1
    $ setWait(96.591,101.436)
    $ speak(NICOLE, "...Wait was I at the wrong locker?")
    stop ambient fadeout 2
    jump scene_0154
label scene_0151:
    $ setVoiceTrack("audio/Scenes/0151.mp3")
    play ambient "audio/Ambience/Neighborhood_Ambience_Night.mp3" fadein 1
    scene onlayer master
    show black
    show home nicole ext night with Pause(2.798):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.798 zoom .6 truecenter
    scene home nicole int
    show nicole pj angry:
        leftcenterstage

    show jecka pj unhappy:
        rightcenterstage
    play ambient "audio/Ambience/House_Night_Ambience.mp3"
    $ setWait(2.798,5.008)
    $ speak(JECKA, "Yeah they really need a lock on that door.")
    $ setWait(5.008,8.762)
    $ speak(NICOLE, "Thanks hindsight, so what the fuck do I do right now? This is gonna ruin my life.")
    $ setWait(8.762,10.681)
    $ speak(JECKA, "Why can't you tell the principal, again?")
    $ setWait(10.681,15.686)
    $ speak(NICOLE, "Cause that's fucking embarrassing? Ms. Lynn, that mean boy has a picture of my titties halfway out!")
    $ setWait(15.686,18.73)
    $ speak(JECKA, "Yeah they'll probably find a way to make it your fault anyway.")
    $ setWait(18.73,26.405)
    $ speak(NICOLE, "I still can't believe he shot it on medium format film of all things. What kind of pretentious dipshit jerks off to film prints?")
    $ setWait(26.405,31.91)
    $ speak(JECKA, "Our parents in the 70's-- wait.. like film film? Like it needs to be developed?")
    show nicole pj:
        leftcenterstage
    $ setWait(31.91,34.997)
    $ speak(NICOLE, "Yeah he said he was getting it developed at tomorrow's film club.")
    show jecka pj:
        rightcenterstage
    $ setWait(34.997,41.753)
    $ speak(JECKA, "Break in that bitch! No lab no developing. If it's some weird format there won't be another one for miles and miles, right?")
    $ setWait(41.753,45.132)
    $ speak(NICOLE, "Destroying the dark room.. would I get expelled for that?")
    $ setWait(45.132,50.929)
    $ speak(JECKA, "If you go in after everybody leaves no one needs to know. Just wear gloves or something so you don't leave fingerprints.")
    $ setWait(50.929,54.641)
    $ speak(NICOLE, "Gloves? If I have any. ...Will you go with me?")
    show jecka pj unhappy:
        rightcenterstage
    $ setWait(54.641,56.685)
    $ speak(JECKA, "No, it's not my ass on film.")
    show nicole pj angry:
        leftcenterstage
    $ setWait(56.685,58.395)
    $ speak(NICOLE, "Come on, I'd help if it was you!")
    show jecka pj angry:
        rightcenterstage
    $ setWait(58.395,60.314)
    $ speak(JECKA, "No you wouldn't.")
    $ setWait(60.314,63.108)
    $ speak(NICOLE, "..Okay I wouldn't but. God dammit.")
    show jecka pj unhappy:
        rightcenterstage
    $ setWait(63.108,66.987)
    $ speak(JECKA, "Is it really the end of the world if people see you in your underwear? You look good naked.")
    $ setWait(66.987,71.825)
    $ speak(NICOLE, "Yeah exactly. If I had weird tits and a gut it'd be classified as an \"artistic nude\".")
    $ setWait(71.825,73.911)
    $ speak(JECKA, "But if you're hot with no clothes on--")
    show nicole pj:
        leftcenterstage
    $ setWait(73.911,75.162)
    $ speak(NICOLE, "It's porn.")
    $ setWait(75.162,79.041)
    $ speak(JECKA, "Ugh fine I'll drive you over there. But I'm not stepping a foot inside that place.")
    show nicole pj:
        leftcenterstage
        linear 2.5 off_right

    show jecka pj unhappy:
        rightcenterstage
        pause 1.2
        xzoom -1
        linear 2 off_right
    $ setWait(79.041,80.918)
    $ speak(NICOLE, "Let's go.")
    stop ambient fadeout 2
    jump scene_0152
label scene_0152:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.6 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0152.mp3")
    play ambient "audio/ambience/darkroom_ambience.mp3" fadein 1.7
    scene dark room
    show nicole pj gloves:
        centerstage
        xzoom -1
    $ setWait(0.134,3.92)
    $ speak(NICOLE, "Wow I am creative when it comes to destroying things.")
    $ setWait(3.92,5.047)
    $ speak(JECKA, "Are you done yet?")
    $ setWait(5.047,9.801)
    $ speak(NICOLE, "Yeah just about, this should buy me enough time to swipe Jeffery's camera and ruin the negatives")

    show white onlayer screens:
        alpha 1.0
        pause 0.07
        alpha 0.0
        pause .07
        alpha 1.0
        pause .07
        alpha 0.0

    show nicole pj gloves scared:
        xalign 0.38
        xzoom 1
        linear 0.2 xalign 0.2

    show cop:
        off_right
        pause 1
        linear .8 rightstage
    $ setWait(9.801,13.43)
    $ speak(COP, "Hey! Do you have permission to be here!?")
    $ setWait(13.43,20.854)
    $ speak(NICOLE, "Uh.. if I said a teacher told me to meet here for a date would you go after him or just blame me for that too?")
    show cop:
        rightstage
        pause 5.5
        linear 0.5 centerstage
    $ setWait(20.854,26.985)
    $ speak(COP, "A date in your pajamas? Did he tell you to destroy thousands in school property too? Look at this place! Come with me!")
    show nicole pj gloves scared:
        xalign 0.2
        linear 0.18 leftstage
    $ setWait(26.985,31.573)
    $ speak(NICOLE, "What!? It was like this when I... sleep walked in here.")
    $ setWait(31.573,33.533)
    $ speak(COP, "You wear gloves to bed?")
    stop ambient fadeout 3
    jump end_0153

label end_0153:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0153" not in persistent.endings:
        $ persistent.endings.append("end_0153")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0153end with Pause (31.8):
        alpha 1.0
    return

label scene_0154:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.6 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0154.mp3")
    play ambient "audio/ambience/school_ext_ambience.mp3" fadein 1.5
    scene school ext 4
    show nicole sc5 angry:
        leftcenterstage

    show jecka sc6 unhappy:
        rightcenterstage
    $ setWait(0.533,3.419)
    $ speak(NICOLE, "So I'm fucked. Totally fucked.")
    $ setWait(3.419,8.34)
    $ speak(JECKA, "Whoa slow down, it's just a picture of you in your underwear? Like no nipples or anything?")
    show nicole sc5 sad:
        leftcenterstage
    $ setWait(8.34,14.722)
    $ speak(NICOLE, "..Now that you're asking I'm suddenly worried one might've been halfway out or something. Does areola count as nipple?")
    $ setWait(14.722,16.306)
    $ speak(JECKA, "Ugh that's a good question.")
    show nicole sc5:
        leftcenterstage
    $ setWait(16.306,22.021)
    $ speak(NICOLE, "Either way, I gotta stop this from being developed. This shit always manages to pop back up in the future.")
    show jecka sc6 angry:
        rightcenterstage
    $ setWait(22.021,25.065)
    $ speak(JECKA, "What future? You say you're gonna kill yourself every other day.")
    $ setWait(25.065,29.695)
    $ speak(NICOLE, "Well I wanna go out as a troubled teen philosopher, not some slut in over her head.")
    show jecka sc6 unhappy:
        rightcenterstage
    $ setWait(29.695,32.114)
    $ speak(JECKA, "Even in death you're manipulative.")
    $ setWait(32.114,36.869)
    $ speak(NICOLE, "Sorry if I don't want my legacy to be freaks jacking off to pictures of me.")
    $ setWait(36.869,43.25)
    $ speak(JECKA, "I would die for half the self-esteem of a girl who just assumes the whole school would jerk off to her.")
    $ setWait(43.25,47.629)
    $ speak(NICOLE, "Do you think I could like persuade Jeffery to just trash the negative?")
    $ setWait(47.629,52.468)
    $ speak(JECKA, "Yeah if you had cat ears, and a tail, and were basically a cartoon.")
    show nicole sc5 angry:
        leftcenterstage
    $ setWait(52.468,54.887)
    $ speak(NICOLE, "Oh yeah he's fucked up I forgot.")
    $ setWait(54.887,58.974)
    $ speak(JECKA, "May as well focus on damage control, it's all you can do.")
    show nicole sc5:
        leftcenterstage
    $ setWait(58.974,62.019)
    $ speak(NICOLE, "I really hope there's a bomb threat tomorrow.")
    stop ambient fadeout 2
    jump scene_0155
label scene_0155:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 2.6 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0155.mp3")
    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 1.3
    scene school int 1
    show girl_2 color3 unhappy:
        rightstage

    show guy_3 color2:
        rightcenterstage
        xzoom -1
    $ setWait(0.505,5.457)
    $ speak(GIRL_2, "Yeah my brother was asking this girl out for like 3 months.")
    $ setWait(5.457,6.584)
    $ speak(GUY_3, "3 months?")
    $ setWait(6.584,7.543)
    $ speak(GIRL_2, "Yeah.")
    $ setWait(7.543,10.17)
    $ speak(GUY_3, "Did he ask really slowly?")
    show nicole sc8:
        off_left
        linear 4.1 leftcenterstage
    $ setWait(10.17,14.216)
    $ speak(NICOLE, "Okay let's just get through the first day of the rest of my ruined life.")
    show guy_3 color2:
        xzoom 1
    $ setWait(14.216,15.175)
    $ speak(GUY_3, "Hey Nicole!")
    $ setWait(15.175,16.093)
    $ speak(NICOLE, "Here it comes.")
    $ setWait(16.093,19.346)
    $ speak(GUY_3, "Did you see what happened to the photography room?")
    $ setWait(19.346,21.223)
    $ speak(NICOLE, "Oh.. wait what?")
    $ setWait(21.223,28.439)
    $ speak(GUY_3, "There's a big crowd up there, it's all in pieces. All these chemicals combined on the floor too, it's basically mustard gas.")
    show girl_2 color3:
        pause 0.5
        xzoom -1
    $ setWait(28.439,29.481)
    $ speak(JEFFERY, "There she is!")
    show guy_3 color2:
        rightcenterstage
        pause 1
        linear 2 off_left

    show girl_2 color3:
        pause 1.2
        xzoom 1
        rightstage
        linear 2.6 off_left
    $ setWait(29.481,30.733)
    $ speak(GUY_3, "Uh oh, gotta dip!")
    show nicole sc8 surprised:
        leftcenterstage
    $ setWait(30.733,31.942)
    $ speak(NICOLE, "What's going on?")
    show jeffery sc4 angry:
        off_right
        linear 1.6 rightcenterstage

    show lynn:
        off_farright
        linear 1.9 rightstage
    $ setWait(31.942,34.987)
    $ speak(JEFFERY, "Don't play dumb, it's obvious it was you!")
    show nicole sc8:
        leftcenterstage
    $ setWait(34.987,40.2)
    $ speak(LYNN, "Jeffery's given me reason to believe you're the one who destroyed the school photo lab last night.")
    show nicole sc8 angry:
        leftcenterstage
    $ setWait(40.2,44.121)
    $ speak(NICOLE, "Uh, no! I was at home all night mulling over ways to kill myself.")
    $ setWait(44.121,46.415)
    $ speak(LYNN, "In my office, now.")
    stop ambient fadeout 2
    jump scene_0156
label scene_0156:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.8 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0156.mp3")
    play ambient "audio/Ambience/office_ambience.mp3" fadein 1.3
    scene office 2
    show lynn:
        xalign .85

    show nicole sc8 angry:
        xalign .29
    $ setWait(0.10,4.592)
    $ speak(NICOLE, "Just wanna make it clear, one more time, that he has no evidence of me doing this.")
    $ setWait(4.592,15.562)
    $ speak(LYNN, "Well unfortunately, the bread crumbs all lead to you. Trying to stop him from developing his picture of you, albeit unflattering, is not a reason to destroy thousands in school property.")
    $ setWait(15.562,21.609)
    $ speak(NICOLE, "Did you completely glaze over the last 10 things I said? He took a picture in the girls locker room.")
    $ setWait(21.609,31.286)
    $ speak(LYNN, "And I assure you he'll be dealt with soon, but you'll need to learn how to deal with the consequences of revealing attire. Destruction of property is not one of them.")
    $ setWait(31.286,33.079)
    $ speak(NICOLE, "I was in the middle of changing?")
    $ setWait(33.079,37)
    $ speak(LYNN, "You could've been fully nude, it's still unreasonable.")
    $ setWait(37,39.711)
    $ speak(NICOLE, "Wait-- I didn't break anything! Fuck what I was wearing!")
    $ setWait(39.711,45.3)
    $ speak(LYNN, "Out of the 10 students we questioned, no one else had anything close to resembling a motive.")
    $ setWait(45.3,46.801)
    $ speak(NICOLE, "Well go ask 10 more.")

    show nicole sc8 surprised:
        xalign .29

    show kylar sc4:
        xzoom -1
        off_left
        linear 3 xalign 0.56
    $ setWait(46.801,50.43)
    $ speak(KYLAR, "Hey Miss Lynn sorry, just got to school, I'm signing in late again.")
    show nicole sc8:
        xalign .29
    $ setWait(50.43,52.056)
    $ speak(LYNN, "In the middle of something here.")
    show kylar sc4:
        xalign 0.56
        pause 0.5
        xzoom 1
    $ setWait(52.056,58.104)
    $ speak(KYLAR, "Oh with a student-- Nicole? Hey I did the video! You better make good with that pool party plus one.")
    $ setWait(58.104,59.105)
    $ speak(NICOLE, "What video?")
    $ setWait(59.105,62.942)
    $ speak(KYLAR, "Ugh, you don't remember? If I posted a viral video you'd let me go with you?")
    $ setWait(62.942,64.11)
    $ speak(LYNN, "What is this? Get out!")
    $ setWait(64.11,66.237)
    $ speak(KYLAR, "Nah wait it's only like a minute. See?")
    $ setWait(66.237,67.03)
    $ speak(NICOLE, "Yeah?")
    show text kylar 1
    $ setWait(67.03,72.285)
    $ speak(KYLAR, "Yo what's up this is Kylar, let's break this gay ass photo lab!")
    hide text
    show nicole sc8 surprised:
        xalign .29
    $ setWait(72.285,73.703)
    $ speak(NICOLE, "Oh my god.")
    show text kylar 1
    $ setWait(73.703,78.291)
    $ speak(KYLAR, "Fuck photography! It's for people who like animals!")
    hide text
    show nicole sc8:
        xalign .29
        pause 1.72
        xzoom -1
        linear 1.2 off_left
    $ setWait(78.291,82.253)
    $ speak(LYNN, "Nicole leave my office, Kylar could I have a word with you?")
    show kylar sc4:
        xzoom -1
    $ setWait(82.253,83.212)
    $ speak(KYLAR, "Yeah what's up?")
    show black onlayer screens:
        alpha 0
        pause 1.3
        linear 1.8 alpha 1.0

    stop ambient fadeout 2.4
    $ setWait(83.212,86.475)
    $ speak(LYNN, "You're expelled!")
    scene school int 1
    show black onlayer screens:
        alpha 1
        pause 0.3
        linear 2 alpha 0.0
    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 1
    show girl_5 color2:
        leftcenterstage

    show guy_2 color2 smirk:
        xzoom -1
        leftstage

    show crispin sc4:
        rightstage
        linear 3.5 rightcenterstage
    $ setWait(86.475,88.885)
    $ speak(GIRL_5, "Did you see Kylar's video?")

    $ setWait(88.885,90.47)
    $ speak(GUY_2, "No what? What's the deal with it?")
    show girl_5 color2:
        leftcenterstage
        pause 0.6
        linear 0.7 xalign 0.23

    show crispin sc4:
        rightcenterstage
        pause 0.8
        linear 0.75 xalign 0.48

    $ setWait(90.47,93.056)
    $ speak(GIRL_5, "Here watch it on my phone.")
    show nicole sc8 surprised:
        off_right
        xzoom -1
        linear 2.2 xalign 0.78

    show crispin sc4:
        xalign 0.48
        pause 2.15
        xzoom -1

    $ setWait(93.056,96.392)
    $ speak(CRISPIN, "Heh crazy, right? ..Right, Nicole?")
    stop ambient fadeout 7

    show nicole sc8:
        xzoom -1
        xalign 0.78
    show black:
        alpha 0.0
        pause 4
        linear 3.5 alpha 1.0
    $ setWait(96.392,105.248)
    $ speak(NICOLE, "Huh? Yeah.. he did it.. He really did it...")

    jump scene_0157
label scene_0157:
    $ setVoiceTrack("audio/Scenes/0157.mp3")
    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 2
    scene onlayer master
    show black

    show title_june2009 onlayer screens:
        alpha 0.0
        linear .2 alpha 1.0

    show school front with Pause(2.923):
        zoom 1.0 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.923 zoom 1.1 truecenter
    scene school ext 2
    hide title_june2009 onlayer screens
    show girl_4:
        off_right
        linear 6.6 off_farleft

    show guy_1:
        off_farright
        linear 6.6 off_left
    $ setWait(2.923,6.051)
    $ speak(GIRL_4, "The music of our year was pretty special when you think about it.")
    show nicole sc9:
        off_left
        linear 3.5 leftcenterstage
    $ setWait(6.051,9.971)
    $ speak(GUY_1, "Yeah Soulja Boy wasn't a one-hit-wonder, who knew?")
    show nicole sc9:
        xzoom -1
    $ setWait(9.971,13.642)
    $ speak(NICOLE, "I wonder which of them is gonna die first after high school.")
    show jeffery black:
        off_right
        linear 2.3 rightcenterstage

    show nicole sc9:
        pause 0.6
        xzoom 1
    $ setWait(13.642,19.481)
    $ speak(JEFFERY, "Hey Nicole, I know we had our differences here and there but... sign my year book?")

    menu:
        "WRITE SOMETHING MEAN":
            jump scene_0158
        "TELL HIM WHAT EVERY GIRL\nWILL TELL HIM IN COLLEGE":
            jump scene_0159
label scene_0158:
    $ setVoiceTrack("audio/Scenes/0158.mp3")
    scene onlayer master
    show school ext 2
    show yearbook with Pause (14.01):
        alpha 1.0
    stop ambient fadeout 2
    jump scene_0160
label scene_0159:
    $ setVoiceTrack("audio/Scenes/0159.mp3")
    scene school ext 2
    show nicole sc9:
        leftcenterstage

    show jeffery black:
        rightcenterstage
    $ setWait(0.043,2.1)
    $ speak(NICOLE, "No.")
    $ setWait(2.1,2.9)
    $ speak(JEFFERY, "W-what?")
    $ setWait(2.9,4.6)
    $ speak(NICOLE, "No.")
    stop ambient fadeout 1.7
    jump scene_0160
label scene_0160:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.8 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0160.mp3")
    scene gym 4
    play ambient "audio/ambience/gym_ceremony_ambience.mp3" fadein 2
    show lynn:
        xzoom -1
        xalign .85
        pause 11.5
        xzoom 1
        linear 2.8 centerstage
        xzoom -1

    show jeffery grad:
        off_left
        xzoom -1
        pause 11
        linear 4 xalign 0.85

    show podium:
        xalign 0.95

    $ setWait(0.13,17.523)
    $ speak(LYNN, "And once again, I can't even begin to describe how proud I am of each and every one of you. Representing your class with a speech, your valedictorian.")
    show jeffery grad:
        xalign .85
        xzoom -1

    show lynn:
        xzoom -1
        centerstage
    $ setWait(17.523,29.827)
    $ speak(JEFFERY, "Ahem! Thank you Principal Lynn and the rest of the faculty, declaring me the valedictorian for Class of '09. School work was always important to me during my tenure here")
    $ setWait(29.827,32.955)
    $ speak(GUY_3, "Shut the fuck up!")
    show jeffery grad:
        pause 4
        xzoom 1
    $ setWait(32.955,37.96)
    $ speak(JEFFERY, "Anyway, perhaps another among us could put it better.. Nicole?")
    $ setWait(37.96,38.919)
    $ speak(NICOLE, "That's okay.")
    show lynn:
        centerstage
        linear 0.28 xalign 0.87
        pause 1.1
        xzoom 1
        pause 2.3
        linear 1.8 centerstage
        xzoom -1

    show jeffery grad:
        xalign .85
        pause 0.2
        linear 0.2 xalign .6
        pause 2.3
        linear 2.6 off_left

    show nicole grad:
        off_left
        pause 2.5
        linear 2.8 xalign .845
    $ setWait(38.919,44.341)
    $ speak(LYNN, "Nicole, say a few words.")
    show nicole grad:
        xalign .845

    show lynn:
        xzoom -1
        centerstage

    hide jeffery
    $ setWait(44.341,53.433)
    $ speak(NICOLE, "First I'd like to thank our female authority figure Miss Lynn, along with her cleavage for symbolizing how the men at this school have treated me here...")
    $ setWait(53.433,55.811)
    $ speak(NICOLE, "Like a sex object.")
    show lynn:
        centerstage
        linear 0.2 xalign 0.62
    $ setWait(55.811,56.603)
    $ speak(LYNN, "What're you doing!?")
    $ setWait(56.603,63.777)
    $ speak(NICOLE, "In my 2 years here, a good 20%% of the staff has either asked me on a date or made some other form of sexual advance.")
    $ setWait(63.777,68.991)
    $ speak(NICOLE, "I told their supervisors and they said to get my grades up.")
    $ setWait(68.991,70.659)
    $ speak(LYNN, "Are you out of your fucking mind?")
    show lynn:
        xalign .62
        pause 0.3
        xzoom 1
        linear 1.4 off_left
    $ setWait(70.659,72.286)
    $ speak(MOM, "I sent my daughter here!?")
    show black onlayer screens:
        alpha 0
        pause 2.4
        linear 2.5 alpha 1.0

    show nicole grad:
        xalign .845
        pause 3
        xzoom -1
        linear 6 off_left

    stop ambient fadeout 7.25
    $ setWait(72.286,80.4)
    $ speak(COP, "What kinda school is this!? I'm calling the news!")
    scene office 2
    show black onlayer screens:
        alpha 1
        linear 1.8 alpha 0.0
    play ambient "audio/ambience/office_ambience.mp3" fadein 1.5

    show nicole sc10:
        off_left
        linear 2 leftstage

    show lynn shirt:
        xzoom -1
        rightstage
    $ setWait(80.4,87.301)
    $ speak(NICOLE, "Oh oops I was just dropping off my lost textbook check.. awkward.")
    show lynn shirt:
        xzoom 1
    $ setWait(87.301,89.761)
    $ speak(LYNN, "I was on my way out, just packing.")
    $ setWait(89.761,92.222)
    $ speak(NICOLE, "They make you clear the whole room at the end of every year?")
    $ setWait(92.222,96.435)
    $ speak(LYNN, "Uh no, they make you clear the whole room out after you're fired.")
    $ setWait(96.435,97.394)
    $ speak(NICOLE, "Whoops.")
    $ setWait(97.394,100.022)
    $ speak(LYNN, "Your apathy won't work on me, Nicole.")
    show nicole sc10 surprised:
        leftstage
    $ setWait(100.022,101.481)
    $ speak(NICOLE, "You're not mad?")
    $ setWait(101.481,107.321)
    $ speak(LYNN, "No actually, it's been a long time coming. Surprised it didn't happen sooner to be honest.")
    $ setWait(107.321,110.782)
    $ speak(NICOLE, "So you knew ignoring it would come back to bite you?")
    $ setWait(110.782,119.416)
    $ speak(LYNN, "When you've fooled around with half your staff they don't take you very seriously. I know I might seem old to you but we're actually not too different.")
    show nicole sc10:
        leftstage
    $ setWait(119.416,121.752)
    $ speak(NICOLE, "Using our looks to fuck around with people?")
    $ setWait(121.752,124.838)
    $ speak(LYNN, "That's right, been doing it since I was your age.")
    $ setWait(124.838,133.639)
    $ speak(LYNN, "Though you really one upped me. Never letting your emotions trick you into thinking you owed them anything. Rare for a girl your age.")
    $ setWait(133.639,136.183)
    $ speak(NICOLE, "How long for you to figure that out?")
    show lynn shirt:
        rightstage
        linear 3 rightcenterstage
    $ setWait(136.183,146.234)
    $ speak(LYNN, "I still haven't, in 39 years. 39 years old and I didn't report teachers for asking students out because I didn't wanna look stuck up.")
    $ setWait(146.234,151.114)
    $ speak(LYNN, "Sometimes all it takes is one night with someone to feel the need to be loyal.")
    $ setWait(151.114,153.367)
    $ speak(NICOLE, "Ew-- you fucked the counselor!?")
    $ setWait(153.367,155.827)
    $ speak(LYNN, "Ugh, among others.")
    $ setWait(155.827,164.002)
    $ speak(NICOLE, "Well... I guess it only makes sense that men impulsive enough to fuck their boss would also try to fuck kids. I thought you hosted the feminism club?")
    $ setWait(164.002,169.383)
    $ speak(LYNN, "Politics are fashion. We picket for a sense of belonging, not change.")
    $ setWait(169.383,171.593)
    $ speak(NICOLE, "Most of us anyway.")
    show lynn shirt:
        rightcenterstage
        linear 4 off_left
    $ setWait(171.593,177.265)
    $ speak(LYNN, "Maybe one day you'll start your own movement.")
    show nicole sc10:
        leftstage
        linear 5 rightcenterstage
    $ setWait(177.265,180.132)
    $ speak(NICOLE, "...I already have.")
    stop ambient fadeout 2.5
    jump end_0161

label end_0161:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0161" not in persistent.endings:
        $ persistent.endings.append("end_0161")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0161end with Pause (67.7):
        alpha 1.0
    return

label scene_0162:
    $ setVoiceTrack("audio/Scenes/0162.mp3")
    play ambient "audio/ambience/school_ext_ambience.mp3" fadein 1.5
    scene onlayer master
    show black

    show title_april2008 onlayer screens:
        alpha 0.0
        linear .2 alpha 1.0

    show school front with Pause(2.751):
        zoom 1.0 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.751 zoom 1.05 truecenter
    scene school ext 3
    hide title_april2008 onlayer screens
    show jecka sc5 unhappy:
        rightcenterstage

    show nicole sc4:
        leftcenterstage
    $ setWait(2.751,6.63)
    $ speak(JECKA, "But whatever now my Mom's addicted to heroin again, how was your spring break?")
    $ setWait(6.63,11.468)
    $ speak(NICOLE, "Exhausting. I thought everyone would just forget about the hang out promises I made over the winter.")
    $ setWait(11.468,15.556)
    $ speak(JECKA, "The thing where you tell 'em you're really busy for mid-terms but should have time in the spring?")
    $ setWait(15.556,17.474)
    $ speak(NICOLE, "Yeah I thought most of them would just forget.")
    $ setWait(17.474,20.602)
    $ speak(JECKA, "Not when you're hot. They never forget when you're hot.")
    $ setWait(20.602,21.478)
    $ speak(NICOLE, "I'm hot?")
    show jecka sc5:
        rightcenterstage
    $ setWait(21.478,23.021)
    $ speak(JECKA, "You fish for compliments?")
    $ setWait(23.021,30.487)
    $ speak(NICOLE, "Whatever yeah so not a single free day to myself, having to meet dipshits X, Y, and Z at the mall, or the park, or the diner.")
    show jecka sc5 unhappy:
        rightcenterstage
    $ setWait(30.487,33.657)
    $ speak(JECKA, "What kinda mormon-ass bitch meets at a diner?")
    $ setWait(33.657,40.706)
    $ speak(NICOLE, "They all blend together, couldn't tell ya. Worst part is I'm at this point where I'm too nice to even decline the follow-up hangouts.")
    $ setWait(40.706,43.709)
    $ speak(JECKA, "\"Hey let's do this again, maybe next week same time?\"")
    $ setWait(43.709,48.922)
    $ speak(NICOLE, "Yeah so now it's the bullshit I put up with on break combined with the bullshit I put up with at school.")
    $ setWait(48.922,51.508)
    $ speak(JECKA, "Really makes you question the whole point of niceness.")
    $ setWait(51.508,56.68)
    $ speak(NICOLE, "Being nice just traps you into these hostage friendships. Socializing honestly kinda sucks now.")
    $ setWait(56.68,59.266)
    $ speak(JECKA, "You're starting to sound like that weird kid Jeffery.")
    $ setWait(59.266,61.81)
    $ speak(NICOLE, "Yeah, Jeffery's one of my hangouts this week.")
    show jecka sc5 angry:
        rightcenterstage
    $ setWait(61.81,66.106)
    $ speak(JECKA, "Oh my god you're that far in? That's like church girl nice-- tell him to fuck off.")
    show jecka sc5 unhappy:
        rightcenterstage
    $ setWait(66.106,71.195)
    $ speak(NICOLE, "I can't I feel like I'm at a point of no return. If I try to escape now he'll just stalk me.")
    $ setWait(71.195,73.614)
    $ speak(JECKA, "Don't be so cynical, he'll probably just murder you.")
    $ setWait(73.614,77.951)
    $ speak(NICOLE, "Dying would be awesome right now but I feel like there'd be strings attached with him.")
    $ setWait(77.951,80.162)
    $ speak(JECKA, "You're dead, what could he possibly do?")
    $ setWait(80.162,84.958)
    $ speak(NICOLE, "Your body doesn't disappear when you die so whatever his twisted little anime brain wants.")
    $ setWait(84.958,86.251)
    $ speak(JECKA, "Ew okay...")
    $ setWait(86.251,89.588)
    $ speak(JECKA, "But if he actually killed you could I take your body to a taxidermist?")
    $ setWait(89.588,90.714)
    $ speak(NICOLE, "Yes.")
    show jecka sc5:
        rightcenterstage
        pause 1.35
        xzoom -1
        linear 2.5 off_right
    $ setWait(90.714,93.759)
    $ speak(JECKA, "Good to know, have fun with your little dates!")
    stop ambient fadeout 4
    show black:
        alpha 0.0
        pause 1.6
        linear 2.5 alpha 1.0
    $ setWait(93.759,98.72)
    $ speak(NICOLE, "Ugh.")
    jump scene_0163
label scene_0163:
    $ setVoiceTrack("audio/Scenes/0163.mp3")
    play ambient "audio/Ambience/Neighborhood_Ambience_Night.mp3" fadein 1
    scene onlayer master
    show black
    show home nicole ext night with Pause(2.756):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.756 zoom .6 truecenter
    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3"
    show nicole sc5:
        leftcenterstage

    show crispin sc4:
        xzoom -1
        rightcenterstage
        linear 3.2 rightstage
    $ setWait(2.756,5.05)
    $ speak(CRISPIN, "...So this is your place huh?")
    $ setWait(5.05,6.968)
    $ speak(NICOLE, "That's the third time you said that.")
    show crispin sc4:
        xzoom 1
    $ setWait(6.968,10.347)
    $ speak(CRISPIN, "Sorry yeah today's just been wild, crazy.")
    $ setWait(10.347,12.557)
    $ speak(NICOLE, "That's the fourth time you said that.")
    show crispin sc4:
        rightstage
        pause 1.9
        linear 2 rightcenterstage
    $ setWait(12.557,17.896)
    $ speak(CRISPIN, "Oh uh, pretty sweet your Mom's out of town. You could throw a whole party, right?")
    $ setWait(17.896,21.983)
    $ speak(NICOLE, "If I liked people enough to let them destroy my house then yeah absolutely.")
    $ setWait(21.983,30.116)
    $ speak(CRISPIN, "Aw man don't be a downer. You kinda remind me of this one girl from a local punk band around here. She gets kinda stand-offish too.")
    $ setWait(30.116,31.534)
    $ speak(NICOLE, "I'm stand-offish?")
    $ setWait(31.534,42.712)
    $ speak(CRISPIN, "N-not like it's a bad thing, just more like the band makes her image that. I think they were called.. uh, man I can't even think right now ha ha.")
    $ setWait(42.712,45.131)
    $ speak(NICOLE, "Has it really only been 20 minutes?")
    $ setWait(45.131,50.637)
    $ speak(CRISPIN, "Hey I just wanted to let you know, you're actually really pretty.")
    $ setWait(50.637,51.471)
    $ speak(NICOLE, "I know.")
    $ setWait(51.471,58.979)
    $ speak(CRISPIN, "Pretty, and like, pretty cool too. Your taste in music, it's like nothing I've ever heard before. You really know your stuff.")
    $ setWait(58.979,62.565)
    $ speak(NICOLE, "No I don't, I had Sean Kingston on for the last hour.")
    $ setWait(62.565,66.736)
    $ speak(CRISPIN, "Humble too, like, you're different.")
    $ setWait(66.736,68.071)
    $ speak(NICOLE, "I'm not having sex with you.")
    show crispin sc4 unhappy:
        rightcenterstage
    $ setWait(68.071,74.869)
    $ speak(CRISPIN, "Whoa what're you talking about? Fucking you was like the last thing on my mind... unless you'd want to?")
    $ setWait(74.869,78.873)
    $ speak(NICOLE, "You've worn the same Volcom socks for like 2 weeks.")
    stop ambient fadeout 5
    show black:
        alpha 0.0
        pause 2.6
        linear 2 alpha 1.0
    $ setWait(78.873,84.503)
    $ speak(CRISPIN, "...So that's a no? --It's cool if it is.")
    jump scene_0164
label scene_0164:
    $ setVoiceTrack("audio/Scenes/0164.mp3")
    play ambient "audio/Ambience/exterior_ambience.mp3" fadein 1.2
    scene onlayer master
    show black
    show barcade ext with Pause(2.913):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.913 zoom .6 truecenter

    scene barcade int
    play ambient "audio/ambience/barcade_ambience.mp3"
    show nicole sc8 angry:
        xalign 0.4

    show kylar sc4:
        xalign 0.81
    $ setWait(2.913,7.626)
    $ speak(KYLAR, "But yeah, it might seem crowded now but you should see this place on Friday.")
    $ setWait(7.626,8.377)
    $ speak(NICOLE, "What?")
    show kylar sc4:
        xalign 0.81
        linear 2.8 xalign 0.75
    $ setWait(8.377,11.797)
    $ speak(KYLAR, "I said you should see this place on Friday!")
    $ setWait(11.797,12.839)
    $ speak(NICOLE, "Okay.")
    $ setWait(12.839,16.802)
    $ speak(KYLAR, "You see me at the hoops machine? I'm sick, you couldn't keep up!")
    $ setWait(16.802,21.264)
    $ speak(NICOLE, "Yeah I really should've taken it more seriously, I'm 17 after all.")
    $ setWait(21.264,26.103)
    $ speak(KYLAR, "And the ski ball machine? Don't take it too hard, I make everyone look trash at it.")
    $ setWait(26.103,28.355)
    $ speak(NICOLE, "All of this behavior is telling.")
    $ setWait(28.355,31.483)
    $ speak(KYLAR, "Yeah telling pussy ass bitches to suck my dick.")
    stop ambient fadeout 6
    show black:
        alpha 0.0
        pause 3.4
        linear 2 alpha 1.0
    $ setWait(31.483,37.947)
    $ speak(KYLAR, "I think I should start making rap songs, my Dad has a Mac Book.")
    jump scene_0165
label scene_0165:
    $ setVoiceTrack("audio/Scenes/0165.mp3")
    play ambient "audio/ambience/exterior_ambience.mp3" fadein 2
    scene onlayer master
    show black
    show diner ext with Pause(2.755):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.755 zoom .58 truecenter
    scene diner int
    play ambient "audio/ambience/diner_ambience.mp3"
    show nicole sc9:
        xzoom -1
        rightstage

    show jeffery sc3:
        xzoom -1
        rightcenterstage
    $ setWait(2.755,6.842)
    $ speak(JEFFERY, "But yeah season 4? Not really for me personally, how bout you?")
    show nicole sc9 surprised:
        xzoom -1
        rightstage
    $ setWait(6.842,8.844)
    $ speak(NICOLE, "Sorry season 4 of what now?")
    show nicole sc9:
        xzoom -1
        rightstage
    $ setWait(8.844,12.848)
    $ speak(JEFFERY, "The Doki Daisuke anime! You've been paying attention, right?")
    $ setWait(12.848,18.771)
    $ speak(NICOLE, "To the first 3 seasons or you talking for the last 20 minutes?\nActually it's the same answer for both.")
    $ setWait(18.771,27.989)
    $ speak(JEFFERY, "Yeah I know, what were the writers thinking? I'm actually involved with an online group and we're gonna reanimate season 4 the way the fans wanted it!")
    $ setWait(27.989,29.74)
    $ speak(NICOLE, "Like a whole cartoon?")
    show jeffery sc3 happy:
        xzoom -1
        rightcenterstage
    $ setWait(29.74,33.327)
    $ speak(JEFFERY, "Yeah you wanna join? We could use all the help we can get.")
    $ setWait(33.327,39.25)
    $ speak(NICOLE, "I guess. Animation takes a lot of time, right? At least you weird kids put your time toward something.")
    show jeffery sc3:
        xzoom -1
        rightcenterstage
    $ setWait(39.25,47.508)
    $ speak(JEFFERY, "Oh well actually we haven't found an animator yet. Yeah but one of our friend's cousins might do it after he graduates from media school.")
    $ setWait(47.508,48.634)
    $ speak(NICOLE, "For free?")
    show jeffery sc3 happy:
        xzoom -1
        rightcenterstage
    $ setWait(48.634,50.511)
    $ speak(JEFFERY, "Yeah just for the love of the show.")
    $ setWait(50.511,52.471)
    $ speak(NICOLE, "Oh okay, I'm not joining then.")
    show jeffery sc3:
        xzoom -1
        rightcenterstage
    $ setWait(52.471,54.098)
    $ speak(JEFFERY, "Huh? Why not?")
    $ setWait(54.098,58.811)
    $ speak(NICOLE, "There's no difference whether I join or not join because this will never be made.")
    $ setWait(58.811,63.232)
    $ speak(JEFFERY, "Well if you feel that way... Do you know why it's so hard to find animators?")
    $ setWait(63.232,67.361)
    $ speak(NICOLE, "I don't know why the fuck I'm here. I even had to pay for my own shitty cheeseburger.")
    $ setWait(67.361,71.365)
    $ speak(NICOLE, "I'm gonna start telling men I'm vegan so they stop trying to take me places.")
    stop ambient fadeout 2
    jump scene_0166
label scene_0166:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.8 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0166.mp3")
    play ambient "audio/Ambience/Cafeteria_Ambience.mp3" fadein 1.5
    scene cafeteria int
    show nicole sc6 sad:
        xalign .24
        xzoom -1

    show girl_2 color3 unhappy:
        xalign .75

    show jecka sc7 unhappy:
        xalign .52
        xzoom -1
    $ setWait(0.081,4.043)
    $ speak(JECKA, "But yeah Kelly's a fucking whore and I hope she dies, end of discussion.")
    show jecka sc7 unhappy:
        xalign .52
        pause 2.5
        xzoom 1
    $ setWait(4.043,8.297)
    $ speak(GIRL_2, "I'm not opposed to that stance. How bout you, Nicole? .. Nicole?")
    show nicole sc6 surprised:
        xalign .24
        xzoom 1
    $ setWait(8.297,12.635)
    $ speak(NICOLE, "Huh? --Oh sorry I'm exhausted, somehow.")
    show nicole sc6:
        xalign .24
        xzoom 1
    $ setWait(12.635,14.72)
    $ speak(GIRL_2, "You've been tuning out all lunch.")
    $ setWait(14.72,18.349)
    $ speak(JECKA, "She's been down the being nice rabbit hole since spring break.")
    $ setWait(18.349,19.517)
    $ speak(GIRL_2, "Poor new kid.")
    $ setWait(19.517,24.73)
    $ speak(NICOLE, "It's like you know they wanna fuck, but they won't just ask so you can reject them and put an end to the \"friendship\".")
    $ setWait(24.73,27.817)
    $ speak(GIRL_2, "How'd you even let it get to the point of a \"friendship\" anyway?")
    $ setWait(27.817,30.987)
    $ speak(NICOLE, "Cause I'm a fucking pushover, okay? Thank you for reminding me!")
    $ setWait(30.987,35.491)
    $ speak(JECKA, "Oh now don't be a bitch about it, let's just enjoy our cancerous meatloaf in peace.")
    $ setWait(35.491,37.743)
    $ speak(NICOLE, "Fine, sorry.")
    show crispin sc5:
        xzoom -1
        off_left
        linear 2 leftstage

    show nicole sc6:
        pause 1
        xzoom -1
    $ setWait(37.743,40.288)
    $ speak(CRISPIN, "Oh Nicole, what's up? Still on for tonight?")
    show jecka sc7 angry:
        xalign .52
    $ setWait(40.288,42.79)
    $ speak(JECKA, "Fucking Crispin?")
    show crispin sc5 unhappy:
        leftstage
    $ setWait(42.79,43.791)
    $ speak(CRISPIN, "What about me?")
    show jecka sc7 unhappy:
        xalign .52
    $ setWait(43.791,45.626)
    $ speak(NICOLE, "Don't worry about it-- yeah I think so.")
    show crispin sc5:
        leftstage
        pause 0.9
        xzoom 1
        linear 3 off_left
    $ setWait(45.626,49.171)
    $ speak(CRISPIN, "Cool, the concert's gonna be sick with you there.")
    show nicole sc6:
        xzoom 1
    $ setWait(49.171,51.09)
    $ speak(NICOLE, "Shit that concert was tonight?")
    $ setWait(51.09,52.633)
    $ speak(GIRL_2, "You are exhausted.")
    $ setWait(52.633,53.801)
    $ speak(JECKA, "Who's playing?")
    $ setWait(53.801,56.012)
    $ speak(NICOLE, "Literal nobodies, just cover bands.")
    $ setWait(56.012,57.597)
    $ speak(GIRL_2, "Why would you agree to that?")
    $ setWait(57.597,59.473)
    $ speak(JECKA, "She's in too deep to say no.")
    $ setWait(59.473,62.768)
    $ speak(GIRL_2, "Yeah someone told me they saw you at a place with that weird Japan kid.")
    $ setWait(62.768,64.854)
    $ speak(JECKA, "Wow you actually went through with that.")
    $ setWait(64.854,66.522)
    $ speak(GIRL_2, "You need to have some kind of limit.")
    show nicole sc6 sad:
        xalign .24
    $ setWait(66.522,71.944)
    $ speak(NICOLE, "How can I rank who and who not to hang out with when they're all equally shitty to me?")
    $ setWait(71.944,73.237)
    $ speak(JECKA, "Are you suicidal?")
    $ setWait(73.237,75.489)
    $ speak(GIRL_2, "Oh my god don't just ask that.")
    $ setWait(75.489,77.074)
    $ speak(JECKA, "Seriously though...")
    $ setWait(77.074,78.409)
    $ speak(NICOLE, "Yes. Very.")
    $ setWait(78.409,79.452)
    $ speak(JECKA, "Yeah me too.")
    $ setWait(79.452,84.248)
    $ speak(GIRL_2, "Same. But you're not just suicidal you're like depressed too.")
    $ setWait(84.248,86.208)
    $ speak(JECKA, "Maybe you should just blow off that concert.")
    $ setWait(86.208,88.044)
    $ speak(NICOLE, "But then I won't hear the end of it.")
    $ setWait(88.044,89.42)
    $ speak(GIRL_2, "Can't please everybody.")
    $ setWait(89.42,93.507)
    $ speak(JECKA, "Well if you're suicidal just go home and kill yourself, then he's the asshole.")
    $ setWait(93.507,95.009)
    $ speak(GIRL_2, "True yeah.")
    stop ambient fadeout 2.5
    menu:
        "GO TO THE CONCERT":
            jump scene_0167
        "STAY HOME AND\nKILL YOURSELF":
            jump scene_0168
label scene_0167:
    $ setVoiceTrack("audio/Scenes/0167.mp3")
    play ambient "audio/Ambience/exterior_ambience.mp3" fadein 1.5
    scene onlayer master
    show black
    show concert ext with Pause(3.333):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 3.333 zoom .6 truecenter
    scene concert
    play ambient "audio/ambience/venue_ambience.mp3"
    show girl_3:
        leftstage
        linear 1.7 off_left

    show nicole sc6:
        leftcenterstage

    show crispin sc5:
        rightcenterstage
    $ setWait(3.333,5.794)
    $ speak(NICOLE, "I thought they played music at concerts.")
    $ setWait(5.794,9.256)
    $ speak(CRISPIN, "Yeah I think they're just doing a sound check.")
    $ setWait(9.256,15.178)
    $ speak(BAND, "And that was our last song of the set, Linkin Dark up next!")
    $ setWait(15.178,16.555)
    $ speak(CRISPIN, "So you having fun?")
    $ setWait(16.555,18.64)
    $ speak(NICOLE, "I'm actually having an aneurysm.")
    show coach 3 drunk smile:
        off_right
        linear 1.9 rightcenterstage

    show crispin sc5 unhappy:
        rightcenterstage
        pause 1.4
        linear 1 rightstage
    $ setWait(18.64,19.933)
    $ speak(COACH, "Hey you.")
    $ setWait(19.933,22.06)
    $ speak(NICOLE, "Mr. Colby? What're you doing here?")
    $ setWait(22.06,23.395)
    $ speak(COACH, "I work here.")
    $ setWait(23.395,27.148)
    $ speak(NICOLE, "Oh I guess you had to find a new job after the school board fired you.")
    $ setWait(27.148,32.904)
    $ speak(COACH, "What're ya talkin' about \"fired\"? I left, moved on to bigger and better things.")
    $ setWait(32.904,38.326)
    $ speak(NICOLE, "No I'm pretty positive you got fired after groping me and 7 other girls.")
    $ setWait(38.326,45.208)
    $ speak(COACH, "Yeah I'm a player, don't remind me. What's say you and me get out of here? I wanna show ya my new ride.")
    $ setWait(45.208,50.589)
    $ speak(NICOLE, "Y'know I'd love to chill in the back seat with a registered sex offender but I might miss the next shitty band so..")
    show coach 3 drunk smile:
        rightcenterstage
        linear 1 xalign 0.62
    $ setWait(50.589,54.843)
    $ speak(COACH, "C'mon Nicole, none of these high school boys are on this level.")
    $ setWait(54.843,57.554)
    $ speak(NICOLE, "I actually prefer 25 seconds of intercourse.")
    show coach 3 drunk angry:
        xalign .62
        linear 1.5 xalign .59
    $ setWait(57.554,59.598)
    $ speak(COACH, "Just shut up and get in my car!")
    show nicole sc6 angry:
        leftcenterstage
        linear 0.3 leftstage
    $ setWait(59.598,61.766)
    $ speak(NICOLE, "No!")
    $ setWait(61.766,72.193)
    $ speak(COACH, "Fine! You think I don't have any pull now that I'm not your gym teacher but think again! My players love me, and they all keep in touch.")
    $ setWait(72.193,73.82)
    $ speak(NICOLE, "Are you threatening me?")
    $ setWait(73.82,76.865)
    $ speak(COACH, "I didn't do anything.. yet.")
    show nicole sc6 angry:
        xzoom -1
        leftstage
        linear .8 off_left
    $ setWait(76.865,78.992)
    $ speak(NICOLE, "Fuck this I'm outta here.")
    stop ambient fadeout 5
    show crispin sc5 unhappy:
        rightstage
        linear 2.8 off_left
    show black:
        alpha 0.0
        pause 2.2
        linear 2.6 alpha 1.0

    $ setWait(78.992,85.332)
    $ speak(CRISPIN, "Wait! You're gonna miss 3 more cover bands!")
    jump scene_0170
label scene_0168:
    $ setVoiceTrack("audio/Scenes/0168.mp3")
    play ambient "audio/Ambience/Neighborhood_Ambience_Night.mp3" fadein 1.7
    scene onlayer master
    show black
    show home nicole ext night with Pause(3.674):
        zoom 0.5 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 3.674 zoom .6 truecenter

    scene home nicole int
    play ambient "audio/Ambience/House_Night_Ambience.mp3"
    show nicole tanktop:
        leftcenterstage
    $ setWait(3.674,11.974)
    $ speak(NICOLE, "Okay that's off, Mom shouldn't be back from her date for another 4 hours so that's plenty of time.")
    show nicole tanktop sad:
        xzoom -1
    $ setWait(11.974,17.354)
    $ speak(NICOLE, "Are you kidding me? I just wanna slice my wrists dramatically and this is killing the whole vibe...")
    show nicole tanktop angry:
        leftcenterstage
        xzoom 1
        pause 2
        xzoom -1
        linear 4 off_left

    show black onlayer screens:
        alpha 0.0
        pause 2.7
        linear 2.2 alpha 1.0

    stop ambient fadeout 5
    $ setWait(17.354,23.194)
    $ speak(NICOLE, "Whatever, I wanna die, doesn't matter how.")
    play ambient "audio/Ambience/House_Night_Ambience.mp3" fadein 2
    show black onlayer screens:
        alpha 1
    $ setWait(23.194,29.241)
    $ speak(MOM, "Nicole? I forgot my wallet just getting it now-- Oh my god! Nicole!")
    $ setWait(29.241,31.16)
    $ speak(NICOLE, "Huh what?")
    $ setWait(31.16,32.912)
    $ speak(MOM, "What did you do to yourself!?")
    $ setWait(32.912,34.914)
    $ speak(NICOLE, "Can I just die in peace?")
    $ setWait(34.914,38.709)
    $ speak(MOM, "Where's the cordless? I'm calling an ambulance! It'll be okay, sweetie!")
    $ setWait(38.709,43.797)
    $ speak(NICOLE, "Yeah it'd be a lot better if you just fucking left.")
    stop ambient fadeout 8
    $ setWait(43.797,52.871)
    $ speak(MOM, "Hello? Yes, my daughter attempted suicide, there's blood everywhere please send someone!")
    jump end_0169

label end_0169:
    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0169" not in persistent.endings:
        $ persistent.endings.append("end_0169")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0169end with Pause (38.8):
        alpha 1.0
    return

label scene_0170:
    $ setVoiceTrack("audio/Scenes/0170.mp3")
    play ambient "audio/Ambience/School_Ext_Ambience.mp3" fadein 2
    scene onlayer master
    show black
    show school front with Pause(2.834):
        zoom 1.0 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.834 zoom 1.1 truecenter
    scene school int 1
    play ambient "audio/Ambience/Hallway_Ambience.mp3"
    show nicole sc7:
        leftcenterstage

    show jecka sc6 unhappy:
        rightcenterstage
    $ setWait(2.834,5.379)
    $ speak(JECKA, "Hey how was the concert last weekend?")
    $ setWait(5.379,6.63)
    $ speak(NICOLE, "Went as expected.")
    $ setWait(6.63,12.678)
    $ speak(JECKA, "Makes sense, so hey you wanna skip 4th period and buy cigarettes off that weird guy that hangs out in front of our school?")
    show nicole sc7 sad:
        leftcenterstage
    $ setWait(12.678,18.058)
    $ speak(NICOLE, "I would but I've just lost the will to do anything. And 4th period's one of my sleeping classes--")
    $ setWait(18.058,22.854)
    $ speak(JECKA, "Come on I can't go alone. We skip all the time together, what if he kidnaps me?")
    $ setWait(22.854,26.274)
    $ speak(NICOLE, "What am I gonna do? Use my tiny arms to rip you from his grasp?")
    show jecka sc6 angry:
        rightcenterstage
    $ setWait(26.274,27.484)
    $ speak(JECKA, "This is bullshit.")
    $ setWait(27.484,28.151)
    $ speak(NICOLE, "What?")
    $ setWait(28.151,33.573)
    $ speak(JECKA, "You blow all your time on these idiots you don't even like and now you can't even hang when it's someone you do like.")
    $ setWait(33.573,39.037)
    $ speak(NICOLE, "I know but like, I'm too far in, it's gonna be a nightmare if I tell everyone to fuck off now.")
    $ setWait(39.037,44.126)
    $ speak(JECKA, "You have a choice to make. It's either me or your hostage friendships. End of discussion.")
    $ setWait(44.126,48.422)
    $ speak(NICOLE, "Fuck.. well now I gotta think if I love you more than I hate being stalked.")
    $ setWait(48.422,52.3)
    $ speak(JECKA, "If you don't have an answer by 4th period, I'll have one for you...")
    show jecka sc6 angry:
        rightcenterstage
        xzoom -1
        linear 2.2 off_right
    $ setWait(52.3,54.97)
    $ speak(JECKA, "See ya, Nicole.")
    show nicole sc7:
        leftcenterstage
    $ setWait(54.97,56.68)
    $ speak(NICOLE, "God I wish I was a lesbian.")
    hide jecka
    show kylar sc5 angry:
        off_right
        linear 2 rightstage
    $ setWait(56.68,58.515)
    $ speak(KYLAR, "You fucking whore!")
    show nicole sc7 angry:
        leftcenterstage
    $ setWait(58.515,61.768)
    $ speak(NICOLE, "No a lesbian--...Didn't I go to an arcade with you, why are you mad?")
    $ setWait(61.768,66.648)
    $ speak(KYLAR, "It's a barcade-- You know why! Everyone in Lacrosse is talking about it!")
    $ setWait(66.648,70.235)
    $ speak(NICOLE, "I don't get it. Is this for Youtube or something?")
    show kylar sc5 furious:
        rightstage
    $ setWait(70.235,72.988)
    $ speak(KYLAR, "You fucked the whole football team!")
    $ setWait(72.988,78.035)
    $ speak(NICOLE, "No I didn't! Wait-- even if I did, why do you care? We weren't even together, fuck off!")
    show kylar sc5 furious:
        rightstage
        linear 1.4 rightcenterstage
    $ setWait(78.035,82.664)
    $ speak(KYLAR, "All those times I took you out and you had the nerve to have sex with everyone but me!")
    show jeffery sc4 angry:
        off_right
        linear 0.9 rightstage
    $ setWait(82.664,83.79)
    $ speak(JEFFERY, "Yeah me too!")
    show guy_2 angry:
        xzoom -1
        off_left
        linear 1 leftstage

    show nicole sc7 angry:
        pause 0.65
        xzoom -1
    $ setWait(83.79,86.752)
    $ speak(GUY_2, "If I knew you were easy I would've tried more when I took you out!")

    show nicole sc7 angry:
        pause 0.4
        xzoom 1
    $ setWait(86.752,90.672)
    $ speak(KYLAR, "I'm done with you, from now on I'm gonna make your life a living hell!")
    $ setWait(90.672,94.217)
    $ speak(JEFFERY, "My cousin's gonna hack your MySpace when I tell him you used me!")
    show nicole sc7 angry:
        xzoom -1
        pause 1.35
        xzoom 1
    $ setWait(94.217,99.014)
    $ speak(NICOLE, "The fuck is this? You all insisted that I hung out with you, not the other way around!")
    $ setWait(99.014,101.6)
    $ speak(KYLAR, "Then why'd you keep doing it if you didn't wanna date, huh?")
    $ setWait(101.6,103.727)
    $ speak(NICOLE, "You kept offering, I was trying to be nice.")
    $ setWait(103.727,109.941)
    $ speak(KYLAR, "Yeah I kept offering to lube up the prude but looks like you were a manipulative slut the whole fucking time!")
    $ setWait(109.941,112.944)
    $ speak(NICOLE, "A grown man actually started a rumor about me.")
    show jeffery sc4 angry:
        pause 0.5
        rightstage
        linear 0.4 xalign .85

    show guy_3 color2 angry:
        off_right
        linear 0.6 xalign 1.1
    $ setWait(112.944,114.488)
    $ speak(GUY_3, "Somebody steal her backpack!")
    show guy_2 angry:
        leftstage
        linear 1 xalign 0.12

    show crispin sc2 unhappy:
        xzoom -1
        off_left
        linear 1.2 xalign -0.13

    show nicole sc7 sad:
        pause 0.5
        xalign 0.39
        xzoom -1
    $ setWait(114.488,116.823)
    $ speak(GUY_2, "Yeah we gotta get our money back somehow!")
    hide nicole sc7
    show nicole sc7 scream onlayer screens:
        xzoom 1
        leftcenterstage
        linear .8 off_right

    show jeffery sc4 angry:
        pause 0.5
        xzoom -1

    show guy_3 color2 angry:
        pause 0.7
        xzoom -1

    show kylar sc5 furious:
        pause 0.4
        xzoom -1
    $ setWait(116.823,118.717)
    $ speak(NICOLE, "I didn't fuck anyone!")
    stop ambient fadeout 3
    menu:
        "RUN HOME TO MOM":
            jump scene_0171
        "RUN TO THE\nCOUNSELOR'S OFFICE":
            jump scene_0172
label scene_0171:
    $ setVoiceTrack("audio/Scenes/0171.mp3")
    play ambient "audio/Ambience/exterior_ambience.mp3" fadein 1.2
    scene onlayer master
    show black
    show home nicole ext day with Pause(2.162):
        zoom 0.8 truecenter
        alpha 0.0
        parallel:
            linear 0.5 alpha 1.0
        parallel:
            linear 2.162 zoom .85 truecenter

    scene home nicole int
    play ambient "audio/ambience/house_ambience.mp3"
    show mom 5:
        leftstage
        pause 4
        linear 1.1 off_left
    $ setWait(2.162,7.376)
    $ speak(MOM, "You need a prescription for Vicodin? This is hardly a buzz.")
    $ setWait(7.376,11.922)
    $ speak(MOM, "Yes hello? ...Oh hey you.")
    show mom 5 concerned:
        off_left
        xzoom -1
        linear 2 leftstage
    $ setWait(11.922,14.049)
    $ speak(MOM, "Oh no, what is it?")
    $ setWait(14.049,18.345)
    $ speak(MOM, "Are you serious? ...I guess I'll have a word yeah.")
    show nicole sc7 sad:
        off_right
        xzoom -1
        linear .6 rightstage
    $ setWait(18.345,19.638)
    $ speak(NICOLE, "Mom, we gotta talk!")
    show mom 5:
        xzoom 1
    $ setWait(19.638,24.184)
    $ speak(MOM, "Shh- Yeah of course... My daughter just walked in.")
    show mom 5 smile:
        leftstage
        linear 1.3 off_left
    $ setWait(24.184,28.605)
    $ speak(MOM, "Okay see you soon... Bye, sexy.")
    show mom 5:
        xzoom -1
        off_left
        linear 1.3 xalign .2
    $ setWait(28.605,31.15)
    $ speak(MOM, "I was just on the phone with your school.")
    $ setWait(31.15,33.819)
    $ speak(NICOLE, "Who at my school are you calling sexy?")
    $ setWait(33.819,36.28)
    $ speak(MOM, "Your principal-- why are you skipping school!?")
    show nicole sc7 angry:
        xzoom -1
        rightstage
    $ setWait(36.28,41.493)
    $ speak(NICOLE, "Mom you don't understand, like 10 guys were about to jump me over a rumor! I had to split out of there.")
    show mom 5 angry:
        xalign .2
    $ setWait(41.493,49.126)
    $ speak(MOM, "I don't care if it was 20 guys, they're considering expulsion for all the times you skipped. I told you to not screw up here!")
    $ setWait(49.126,53.046)
    $ speak(NICOLE, "Mom I can't help it if the pedophile gym teacher's trying to sabotage me!")
    $ setWait(53.046,55.841)
    $ speak(MOM, "This is the first I've heard of any gym teacher.")
    show nicole sc7 scream:
        xzoom -1
        rightstage
    $ setWait(55.841,60.22)
    $ speak(NICOLE, "I told you about it three times, you would've remembered if you weren't always fucked up on Vicodin!")
    show nicole sc7 angry:
        xzoom -1
        rightstage
    $ setWait(60.22,65.559)
    $ speak(MOM, "That's it! ...That's it. You're going back to that school whether you like it or not.")
    show mom 5 angry:
        xalign .2
        linear 3.1 rightcenterstage
    $ setWait(65.559,69.563)
    $ speak(MOM, "If they expel you from there, you're expelled from this home!")
    show nicole sc7 angry:
        rightstage
        linear 2.1 leftstage

    $ setWait(69.563,71.148)
    $ speak(NICOLE, "Fuck this I'm done.")
    show mom 5:
        xzoom 1
    $ setWait(71.148,76.737)
    $ speak(MOM, "Good, lock yourself in your room! It'll be the last time you're seeing it.")
    show nicole sc7:
        linear 1.8 off_left
    $ setWait(76.737,79.239)
    $ speak(NICOLE, "...You got that right.")
    stop ambient fadeout 2
    jump end_0173
label scene_0172:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.8 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0172.mp3")
    play ambient "audio/ambience/office_ambience.mp3" fadein 1.6
    scene office 1
    show couns 3:
        rightstage

    show nicole sc7 sad:
        off_left
        pause 2
        linear 1.6 leftcenterstage
    $ setWait(0.08,3.75)
    $ speak(NICOLE, "Oh you're actually here! Good, I need some help.")
    $ setWait(3.75,6.336)
    $ speak(COUNSELOR, "Nicole, what a pleasant surprise.")
    show nicole sc7:
        leftcenterstage
    $ setWait(6.336,12.843)
    $ speak(NICOLE, "Yeah yeah, um, you're like student relations, right? You can talk to kids and get 'em to calm down?")
    $ setWait(12.843,15.178)
    $ speak(COUNSELOR, "To an extent? What's the matter?")
    $ setWait(15.178,24.062)
    $ speak(NICOLE, "Well see all these guys I hung out with before, who took the hanging out as dating, yeah so they all suddenly wanna kill me cause I won't have sex with them.")
    $ setWait(24.062,31.32)
    $ speak(COUNSELOR, "Kill is a rather strong word, don't you think? Would you say they're more.. upset?")
    show nicole sc7 angry:
        leftcenterstage
    $ setWait(31.32,32.696)
    $ speak(NICOLE, "Why does this matter?")
    $ setWait(32.696,39.745)
    $ speak(COUNSELOR, "Let's try a different angle. Why are they suddenly all expecting this sex at the same time?")
    show nicole sc7:
        leftcenterstage
    $ setWait(39.745,44.166)
    $ speak(NICOLE, "I'd rather not get into it. Long story, really weird and embarrassing.")
    $ setWait(44.166,50.756)
    $ speak(COUNSELOR, "Fair enough. What I'll say is when people find themselves in situations where it's 10 on 1...")
    $ setWait(50.756,55.594)
    $ speak(COUNSELOR, "...it'd be a tad irrational to immediately rule out the conflict being your fault.")
    $ setWait(55.594,58.68)
    $ speak(NICOLE, "No I get that, but the gym teacher, he was at this concert and like--")
    $ setWait(58.68,62.351)
    $ speak(COUNSELOR, "Now hold on. So why are they upset with you, again?")
    show nicole sc7 angry:
        leftcenterstage
    $ setWait(62.351,64.937)
    $ speak(NICOLE, "Because I didn't have sex with them.")
    $ setWait(64.937,72.277)
    $ speak(COUNSELOR, "So sexual frustration, natural for all boys of their age. But what provokes that?")
    $ setWait(72.277,73.278)
    $ speak(NICOLE, "Hormones?")
    $ setWait(73.278,78.659)
    $ speak(COUNSELOR, "Teasing.. Are we being a tease, Nicole?")
    $ setWait(78.659,80.41)
    $ speak(NICOLE, "...And you're actually employed here?")
    show couns 3 smile:
        rightstage
    $ setWait(80.41,84.998)
    $ speak(COUNSELOR, "Don't deflect, you're usually so.. sharing.")
    $ setWait(84.998,86.75)
    $ speak(NICOLE, "How am I sharing?")
    $ setWait(86.75,92.756)
    $ speak(COUNSELOR, "For instance how you shared your body with the varsity football team?")
    show nicole sc7 angry:
        leftcenterstage
        linear .7 xalign 0.2
    $ setWait(92.756,93.632)
    $ speak(NICOLE, "No...")

    $ setWait(93.632,98.971)
    $ speak(COUNSELOR, "Oh now don't be ashamed, you should be proud of your spontaneity.")
    show couns 3 smile:
        rightstage
        linear 5.2 centerstage
    $ setWait(98.971,106.979)
    $ speak(COUNSELOR, "In fact, I think I'll take you out on a personal field trip. I'd love to explore this curious side of you.")
    show nicole sc7 angry:
        xalign .2
        linear 0.4 leftstage
    $ setWait(106.979,109.815)
    $ speak(NICOLE, "Go fuck yourself, I'm seeing the principal.")
    $ setWait(109.815,116.655)
    $ speak(COUNSELOR, "Might not be the best use of your time. Principal Lynn knows too. We all do.")
    show couns 3 smile:
        xzoom -1
        centerstage
        linear 5.2 rightstage


    show nicole sc7:
        leftstage
    $ setWait(116.655,123.203)
    $ speak(COUNSELOR, "The faculty can't hang themselves over protecting one amorous girl, now can they?")
    show nicole sc7:
        leftstage
        pause 1.5
        xzoom -1
        linear 1.15 off_left
    $ setWait(123.203,127.239)
    $ speak(NICOLE, "...I can.")
    stop ambient fadeout 2
    jump end_0173

label end_0173:
    show black onlayer screens with Pause(2):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.5 alpha 0.0

    $ quick_menu = False

    if "end_0173" not in persistent.endings:
        $ persistent.endings.append("end_0173")
        $ persistent.new_ending = True

    scene onlayer master
    show black
    show 0173end with Pause (67.6):
        alpha 1.0
    return

label end:
    return

label scene_0999:
    stop music fadeout 1.5
    $ _game_menu_screen = "pause_menu"
    show black onlayer screens with Pause(2.3):
        alpha 0.0
        linear 1.4 alpha 1.0

    show black onlayer screens:
        alpha 1.0
        linear 1.8 alpha 0.0
    $ setVoiceTrack("audio/Scenes/0999.mp3")
    scene school int 2
    play ambient "audio/Ambience/Hallway_Ambience.mp3" fadein 1
    show jecka sc5 angry:
        leftstage
        xzoom -1
    show nicole sc10:
        off_right
        xzoom -1
        linear 5 leftcenterstage
    $ setWait(0.775,2.377)
    $ speak(JECKA, "Where the fuck were you?")
    $ setWait(2.377,4.045)
    $ speak(NICOLE, "Long story...")
    $ setWait(4.045,6.548)
    $ speak(NICOLE, "...Well no it's actually short I just don't feel like telling you.")
    $ setWait(6.548,11.219)
    $ speak(JECKA, "Okay whatever, can we go now? All the good graduation parties are gonna be out of coke if we go too late.")
    $ setWait(11.219,13.972)
    $ speak(NICOLE, "Is there coke at the bad graduation parties or just the good ones?")
    $ setWait(13.972,15.807)
    $ speak(JECKA, "What do you think makes them good?")
    $ setWait(15.807,18.518)
    $ speak(NICOLE, "I thought you were a pharma-princess since when do you want hard shit?")
    show jecka sc5:
        leftstage
        xzoom -1
    $ setWait(18.518,21.062)
    $ speak(JECKA, "Since we graduated and I don't give a fuck anymore!?")
    $ setWait(21.062,27.819)
    $ speak(JECKA, "Doing coke in high school's depressing but I'm gonna be in college soon. Whose Line Is It Anyway? Mine! I'm Wayne Brady in this bitch, ho!")
    show nicole sc10 smile:
        leftcenterstage
    $ setWait(27.819,32.407)
    $ speak(NICOLE, "You wanna be some cokehead bitch in college? Cause if you do I fully support it, you'd be like ten times hotter.")
    $ setWait(32.407,39.247)
    $ speak(JECKA, "Oh my god I know. I wanna like.. go full out of control and then marry some rich med major who wants to save me. Ultimate goal.")
    show nicole sc10 surprised:
        leftcenterstage
        xzoom -1
    $ setWait(39.247,40.457)
    $ speak(NICOLE, "Is that the ceiling for us?")
    show jecka sc5 unhappy:
        leftstage
        xzoom -1
    show nicole sc10:
        leftcenterstage
        xzoom 1
    show jeffery grad angry:
        off_right
        linear .8 rightstage
    $ setWait(40.457,42.709)
    $ speak(JEFFERY, "What's the big idea, huh!?")
    show jecka sc5:
        leftstage
    $ setWait(42.709,44.294)
    $ speak(JECKA, "I don't know I only have little ideas.")
    show nicole sc10 smile:
        leftcenterstage
    $ setWait(44.294,45.837)
    $ speak(NICOLE, "Yeah and I got medium ideas.")
    show jecka sc5 unhappy:
        leftstage
    show nicole sc10:
        leftcenterstage
    $ setWait(45.837,50.925)
    $ speak(JEFFERY, "You ruined the whole graduation ceremony, I was valedictorian and everything!")
    $ setWait(50.925,57.682)
    $ speak(JEFFERY, "What did anybody do to you anyway? Everybody's always nice to you and calls you pretty and all you wanna do is hurt them!")
    $ setWait(57.682,59.225)
    $ speak(NICOLE, "Well shoot if they call me pretty...")
    $ setWait(59.225,72.614)
    $ speak(JEFFERY, "And more than that! They give you things, always help you, and then I just see you screw them over! All I see is you being mean for the sake of being mean, like it's a game to you!")
    $ setWait(72.614,74.991)
    $ speak(NICOLE, "...You want me to tell you what you don't see?")
    $ setWait(74.991,77.911)
    $ speak(JEFFERY, "I've seen enough.")
    $ setWait(77.911,82.207)
    $ speak(NICOLE, "Have you ever seen a man three times your age ask you to fuck him?")
    $ setWait(82.207,83.625)
    $ speak(JECKA, "Like just this week or?")
    $ setWait(83.625,85.251)
    $ speak(JEFFERY, "Wha-- Be serious!")
    $ setWait(85.251,92.425)
    $ speak(NICOLE, "Sorry, how about 60 texts in one night all threatening you if you don't go out with the pizza delivery man who sent them?")
    $ setWait(92.425,96.513)
    $ speak(JEFFERY, "How would you let some crazy guy get your number like that in the first place?")
    $ setWait(96.513,103.853)
    $ speak(NICOLE, "I ordered pizza with my cell phone. I know your pasty white ass wouldn't get what being in demand is like, but it's a tough job, Jeffery.")
    $ setWait(103.853,105.105)
    $ speak(JECKA, "And you don't even get paid.")
    $ setWait(105.105,108.149)
    $ speak(NICOLE, "But if you do you're a whore. Are you getting it, Jeffery?")
    $ setWait(108.149,110.86)
    $ speak(JEFFERY, "So people like you, boo hoo.")
    $ setWait(110.86,117.158)
    $ speak(NICOLE, "They don't just like us, they're obsessed with us. Obsession leads to a lot of crazy shit...")
    $ setWait(117.158,125.834)
    $ speak(NICOLE, "...and you give the wrong bitch enough crazy shit in her life, she just might snap on everybody.")
    $ setWait(125.834,132.715)
    $ speak(JEFFERY, "Sounds like a good problem to have. I'd rather be surrounded by craziness instead of still being lonely.")
    $ setWait(132.715,139.055)
    $ speak(JEFFERY, "You don't know what that feels like, you don't know what life is like wanting a partner and being ignored by everyone.")
    $ setWait(139.055,142.767)
    $ speak(JEFFERY, "You're spoiled by social attention and you don't even know it.")
    $ setWait(142.767,144.018)
    $ speak(JECKA, "Is this your manifesto?")
    show jeffery grad:
        rightstage
    $ setWait(144.018,144.686)
    $ speak(JEFFERY, "My what?")
    $ setWait(144.686,147.188)
    $ speak(NICOLE, "At least wait 'till we get to college before you kill us, okay?")
    $ setWait(147.188,151.151)
    $ speak(JEFFERY, "I never said I'd do that... \nWhat college you guys going to anyway?")
    show jecka sc5:
        leftstage
    $ setWait(151.151,153.027)
    $ speak(JECKA, "What college are we going to?")
    show nicole sc10 smile:
        leftcenterstage
    $ setWait(153.027,154.028)
    $ speak(NICOLE, "Could be Maryland.")
    $ setWait(154.028,154.737)
    $ speak(JECKA, "Or Florida.")
    $ setWait(154.737,155.78)
    $ speak(NICOLE, "Maybe Cal State.")
    $ setWait(155.78,158.366)
    $ speak(JECKA, "You're gonna have to shoot up every school in the country at this rate.")
    show jeffery grad angry:
        rightstage
    $ setWait(158.366,166.374)
    $ speak(JEFFERY, "Rgh everytime I try having a regular conversation you just make it a joke about me. Like I said, socially spoiled.")
    $ setWait(166.374,167.167)
    $ speak(JECKA, "Little bit.")
    show nicole sc10:
        leftcenterstage
    $ setWait(167.167,170.17)
    $ speak(NICOLE, "Can someone be spoiled by not having a daily fight-or-flight moment?")
    $ setWait(170.17,172.505)
    $ speak(JEFFERY, "Wha-- Like I should be you for a day?")
    show jecka sc5 unhappy:
        leftstage
    $ setWait(172.505,175.633)
    $ speak(JECKA, "You're way too ugly to be her for a day.")
    show jeffery grad:
        rightstage
    $ setWait(175.633,177.51)
    $ speak(JEFFERY, "Well...")
    show jeffery grad angry:
        rightstage

    stop ambient fadeout 8
    $ setWait(177.51,183.683)
    $ speak(JEFFERY, "...she gets too much attention to know how much it hurts to be me for a day.")

    show black onlayer screens:
        alpha 0
        pause 2.6
        linear 3 alpha 1

    show nicole sc10:
        leftcenterstage
        xzoom -1
        linear 5 off_farleft

    show jecka sc5 unhappy:
        leftstage
        pause 2.7
        xzoom 1
        linear 3 off_farleft


    $ setWait(183.683,192.605)
    $ speak(NICOLE, "I guess we'll never know.")


    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
