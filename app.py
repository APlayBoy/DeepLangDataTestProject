import gradio as gr
import traceback


def hello_world_fn(username: str):
    try:
        return f"HELLO WORLD\n{username.upper()}", "SUCCESS"
    except Exception as e:
        return f"opus! some exception {e}\n{traceback.format_exc()}", "FAILED"

def html_parse_fn(html_str: str):
#     <a>
#    111
#    <b>222 </b>
#    <p>
#       333
#       <c>444</c>
#    </p>
#    <p>555</p>
#   </a>
    stack = []
    result = []
    for i, c in enumerate(html_str):
        if c == ">":
            cur_ind = i
            while stack[-1] != "<":
                stack.pop()
                cur_ind = cur_ind - 1
            cur_ind = cur_ind - 1
            stack.append(html_str[cur_ind : i+1])
            #结尾tag
            if html_str[cur_ind+1] == "/":
                begin_tag = '<\\' + stack[-1][2:]
                if stack[-1] == "<\p>":
                    true_text = ''
                    while stack[-1] != begin_tag:
                        true_text += stack.pop()
                    
                    result.append(true_text)
                else:
                    while stack[-1] != begin_tag:
                        stack.pop()
        else:
            stack.append(c)
        
    return true_text


def main() -> None:
    with gr.Blocks(title="DeepLang Data test project") as demo:
        with gr.Tab("hello world 0"):
            raw_input = gr.Textbox(lines=1, placeholder="输入你的名字(英文)", label="")
            pack_output = gr.Textbox(label="输出")
            status_output = gr.Textbox(label="状态信息")

            btn = gr.Button("开始转换")
            btn.click(
                fn=hello_world_fn,
                inputs=raw_input,
                outputs=[pack_output, status_output],
            )

        with gr.Tab("hello world 1"):
            raw_input = gr.Textbox(lines=1, placeholder="输入你的名字(英文)", label="")
            pack_output = gr.Textbox(label="输出")
            status_output = gr.Textbox(label="状态信息")

            btn = gr.Button("开始转换")
            btn.click(
                fn=hello_world_fn,
                inputs=raw_input,
                outputs=[pack_output, status_output],
            )
        
        with gr.Tab("html parser"):
            raw_input = gr.Textbox(lines=1, placeholder="请输入html", label="")
            pack_output = gr.Textbox(label="输出")

            btn = gr.Button("开始解析")
            btn.click(
                fn=html_parse_fn,
                inputs=raw_input,
                outputs=[pack_output],
            )

    demo.queue(default_concurrency_limit=100).launch(
        inline=False,
        debug=False,
        server_name="127.0.0.1",
        server_port=8081,
        show_error=True,
    )


if __name__ == "__main__":
    main()
