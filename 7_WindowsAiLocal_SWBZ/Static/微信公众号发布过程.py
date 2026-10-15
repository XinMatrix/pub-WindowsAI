# ['',
#  f'TAG(8-微信公众号)->'
#  f'WEB_BROWSER_EDGE({start_json('GET', 'WeiXin')})->WAIT_OCR(添加视频)->SLEEP(1)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY(SPACE)->SLEEP(1)->'
#  f'INPUT({start_json('GET', 'VideoPath')})->SLEEP(0.5)->KEY(ENTER)->WAIT_OCR(视频上传成功%)->SLEEP(5)->CLICK_TEXT_RIGHT(从图片库选择,230)->'
#  f'SLEEP(1)->CLICK_TEXT(完成)->SLEEP(1)->ROLL_TO(-500)->CLICK_TEXT(%导出视频)->HOTKEY(CTRL+A)->'
#  f'COPY_TITLE_FROM_JSON({start_json('GET', 'json_path')})->PAST_TEXT()->KEY(TAB)->KEY(TAB)->KEY(TAB)->KEY(SPACE)->'
#  f'CLICK_TEXT_RIGHT(原创声明,50)->CLICK_TEXT(确定)->CLICK_TEXT(保存并发表)->SLEEP(3)->WAIT_OCR(楚门世界指南)->SLEEP(1)->'
#  f'ROLL_TO(-1000)->CLICK_TEXT(赞赏)->SLEEP(3)->CLICK_TEXT(确定)->CLICK_TEXT(留言)->CLICK_TEXT(确定)->'
#  f'CLICK_TEXT(发表)->CLICK_TEXT_LEFT(取消,150)->CLICK_TEXT(继续发表)->WAIT_OCR(微信验证)->FINISH_BACK()']