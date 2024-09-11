import pyui


class TextTest(pyui.View):
    line = pyui.State(default="")
    lines = pyui.State(default="")
    text = pyui.State(default="")

    async def built(self):
        self.text = "some text from http response"

    def content(self):
        yield pyui.VStack(alignment=pyui.Alignment.LEADING)(
            pyui.Text("Enter some text below:"),
            pyui.TextField(self.line, placeholder="Single line text"),
            pyui.TextField(self.lines, placeholder="Two line text input").lines(2),
            pyui.TextField(self.text, placeholder="All the text")
            .lines(None)
            .priority("high"),
            pyui.HStack()(
                pyui.Spacer(),
                pyui.Button("Submit", asset="button.primary"),
            ),
        ).padding(20)


def init() -> None:
    app = pyui.Application("io.temp.TextTest")
    app.window("Text Tester", TextTest())
    app.run()


if __name__ == "__main__":
    init()