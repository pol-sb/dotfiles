import argparse
import subprocess as sb

# Construct an argument parser
all_args = argparse.ArgumentParser()

# Add arguments to the parser
all_args.add_argument("--vol", required=True, help="Increase or decrease volume")
args = vars(all_args.parse_args())

vol = args["vol"]

if vol == "up":
    sb.call(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])
elif vol == "down":
    sb.call(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"])
elif vol == "mute":
    sb.call(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])


vol_curr = sb.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"]).decode(
    "utf-8"
)

vol_val = int(vol_curr.split("/")[1].strip().replace("%", ""))
# print(vol_val)

if vol != "mute":
    sb.call(
        [
            "notify-send",
            "-h",
            f"int:value:{vol_val}",
            "-h",
            "string:x-dunst-stack-tag:test",
            f"Volume: {vol_val}%",
            "-t",
            "1250",
            "-i",
            "/usr/share/icons/Tela-nord/22@2x/panel/audio-volume-high.svg",
        ]
    )

else:
    mute_curr = (
        sb.check_output(["pactl", "get-sink-mute", "@DEFAULT_SINK@"])
        .decode("utf-8")
        .strip()
    )
    mute_curr = mute_curr.split(":")[1].strip()

    if mute_curr == "yes":
        sb.call(
            [
                "notify-send",
                "-h",
                f"int:value:0",
                "-h",
                "string:x-dunst-stack-tag:test",
                #'-h', 'string:bgcolor:#2d1e1e',
                f"Muted",
                "-t",
                "1250",
                "-i",
                "/usr/share/icons/Tela-nord/22@2x/panel/audio-volume-muted-blocking.svg",
            ]
        )

    if mute_curr == "no":
        sb.call(
            [
                "notify-send",
                "-h",
                f"int:value:{vol_val}",
                "-h",
                "string:x-dunst-stack-tag:test",
                f"Unmuted",
                "-t",
                "1250",
                "-i",
                "/usr/share/icons/Tela-nord/22@2x/panel/audio-on.svg",
            ]
        )
