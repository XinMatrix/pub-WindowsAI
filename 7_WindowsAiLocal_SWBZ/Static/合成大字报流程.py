# TODO �ϳɴ��ֱ����̡����Ҹ���Ƶ������ΪʲôҪ���������Ϊ����ֿ��������������ҵ�����
        #  ��ģ�������Ȼ���ٿ�����¼���������ƽ�����������ƽ�������汾̫�ͣ�û�д��ֱ���ֻ��¼���ˡ�����ֻ����8.5.0�����˶�����
        #  ��Ҳ����������Ļ�����һЩ������ʹ��ģ�������ؼ�ֻ������Ƶ�ʶ�����
        #  ���ܻ�Ƚ��鷳��������Ͳ����ˣ�һ�����ݣ�ֻ��ҪBվ��Ƶ��ַ����
        #  ��ǰ���󣬿�����һ����ʼ�����ô������
        # ['',
        #  f'TAG(0-�ϳ���Ƶ-��ӳ��Ļ���ֱ�)->'
        #  # ��ʼ���ļ�
        #  f'INIT_FILES()->'
        #  # ��MuMuģ�����رչ��Ԥ������ģ������Ϊ��ʹ�ñؼ������ı�ת��Ϊ��Ƶ
        #  f'START_PROGRAM_BY_PATH({sj('MumuPath')})->WAIT_OCR(��Ϸ����)->SLEEP(5)->HOTKEY(ALT+F4)->'
        #  # ��JiJiDown����Bվ��Ƶ
        #  f'COPY({sj('VideoLink')})->START_PROGRAM_BY_PATH({sj('JijidownPath')})->WAIT_OCR(���ع���)->KEY(TAB)->KEY(ENTER)->'
        #  f'CLICK_TEXT(MP3��Ƶ�ļ�)->SLEEP(1)->CLICK()->SLEEP(10)->WAIT_MP3({sj('TempFolder')})->HOTKEY(ALT+F4)->'
        #  # ��Ƶת���֣��ƴ�Ѷ��
        #  f'AUDIO_2_TEXT_BY_API({sj('DateFilepath')})->'
        #  # ����Prompt���ɱ��⡢�İ�����ǩ��GPT 3.5
        #  f'START_GPT_API({sj('DateFilepath')})->'
        #  # ���ɷ���
        #  f'GENERATE_COVER({sj('json_path')})->'
        #  # �򿪱ؼ����������ı��ʶ�mp4
        #  f'START_PROGRAM_BY_PATH({sj('MumuPath')})->WAIT_OCR(��Ϸ����)->SLEEP(1)->KEY(F11)->CLICK_TEXT_TOP(�ؼ�,80)->'
        #  f'SET_FOCUS(MuMuģ����12)->CLICK_TEXT(��ɫ��¡)->CLICK_TEXT(��ɫ01)->CLICK_TEXT(ȥ�����ı��ʶ�)->'
        #  f'COPY_TEXT_FROM_JSON({sj('json_path')})->PAST_TEXT()->CLICK_TEXT(�����ʶ���Ƶ)->CLICK_TEXT(����)->'
        #  f'WAIT_OCR(���)->SLEEP(1)->HOTKEY(ALT+F4)->SLEEP(3)->MOVE_TO_MAKE({sj('BuildVideoPath')})->'
        #  # TODO ʹ�ü�ӳ������Ļ�����ȵȣ�������Ҫ��Ļ�ˣ�ֱ�Ӱ����
        #  #  ���ؼ����ɵ���MP3����MP4�������MP3����תΪMP4����ȷ���������ԣ�
        #  #  MOVE_TO_MAKE({sj('BuildVideoPath')})  # Ӧ�ð����ɺõ��ʶ�����Ƶת�ƹ�����Ȼ���ٴ򿪼�ӳ
        #  #  �� file_path ���ҵ����µ���Ƶ���ƶ��� E:\WindowsAi\7_WindowsAiLocal_SWBZ\��ʱ����
        #
        #  # TODO �о����ƣ����������زİɣ���������
        #  #  CTRL+IҲ���Ե����زģ�����û�������
        #  #  OPEN(sj('JianYingPro'))->CLICK_TEXT(��ʼ����)->CLICK_TEXT(%֧��%)->COPY(sj('AudioWithSubtitles'))->PAST_TEXT()->
        #  #  KEY(ENTER)->CLICK_POSITION(280.270)->SLEEP(1)->CLICK()->KEY(TAB)->SLEEP(1)->KEY(TAB)->SLEEP(1)->KEY(TAB)->SLEEP(1)->
        #  #  KEY(TAB)->SLEEP(1)->KEY(TAB)->SLEEP(1)->KEY(TAB)->CLICK_TEXT_RIGHT(ͬʱ���������Ļ,565)->WAIT_OCR_END(ȡ��)->
        #  #  CLICK_TEXT(��Ļģ��)->ROLL_TO(-500)->CLICK_TEXT(��ת����)->CLICK_POSITION(490,280)->SLEEP(1)->CLICK()->
        #  #
        #  # E:\WindowsAi\7_WindowsAiLocal_SWBZ\��ʱ����\��Ƶ����Ļ.mp4
        #  # C:\Users\USER\AppData\Local\JianyingPro\Apps\JianyingPro.exe
        #
        #  # ����ʹ�ñؼ�������Ļ
        #  # f'CLICK_TEXT(����)->CLICK_TEXT(����ת%)->SLEEP(1)->CLICK_POSITION(770,240)->CLICK_TEXT(��һ��)->SLEEP(1)->'
        #  # f'CLICK_TEXT(��ʼʶ��)->CLICK_TEXT(����)->WAIT_OCR(�ѱ���)->SLEEP(3)->HOTKEY(ALT+F4)->MOVE_TO_MAKE({sj('BuildVideoPath')})->'
        #  # �ü�������Ƶ�����ز�
        #  f'CUT_VIDEO()->'
        #  # ����������Ƶ������
        #  f'CREATE_FINAL_VIDEO()->SLEEP(3)->COPY_VIDEO_TO_FOLDER()->UPDATE_VIDEO_PATH()->GIT_REPO()->DELETE_MIDDLE_FILES()->FINISH()']
