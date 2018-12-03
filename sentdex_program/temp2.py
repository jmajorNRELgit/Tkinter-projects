led = tk_tools.Led(frame2, size=50)
        led.grid(row = 3, column = 1)
        led.to_red()
        led.to_green(on=True)