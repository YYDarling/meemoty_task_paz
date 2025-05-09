# === task.py ===
from psychopy import visual, core, event
from utils import generate_trials, save_results
import os
import sys



def run_task(cfg, subject_id, session_num):
    try:
        trials = generate_trials(cfg)
    except AssertionError as e:
        print(f"❌ Error: {e}")
        return

    win = visual.Window([1280, 900], color='grey')
    # win = visual.Window(fullscr=True, color='grey')


    img_stim = visual.ImageStim(win, size=(0.85, 0.85))  # 相对于屏幕大小（1.0 是整屏）
    # count trails
    trial_counter_stim = visual.TextStim(win, pos=(0, 0.6), color='black', height=0.07)

    # button tips
    key_hint_stim = visual.TextStim(
        win, pos=(0, -0.6), color='black', height=0.06,
        text="[B] = New     [N] = Old     [M] = Similar"
    )
    text_stim = visual.TextStim(win, text='', color='white', height=0.06, wrapWidth=1.6)

    # instruction
    instruction = (
        "Welcome to the Cognitive Task!\n"
        "You will see pictures of everyday objects.\n\n"
        "Press 'B' if the item is NEW\n"
        "Press 'N' if the item is OLD\n"
        "Press 'M' if the item is SIMILAR\n\n"
    )

    # === Add mode-specific note
    if cfg['mode'] == 'fixed':
        instruction += "Each picture will be shown for 2 seconds.\n"
        instruction += "Please respond before it disappears.\n\n"
    else:
        instruction += "The task is self-paced — each picture stays until you respond.\n\n"

    instruction += "Press any key to start."

    text_stim.text = instruction
    text_stim.draw()
    win.flip()

    # ✅ 检测窗口是否被关闭（如点击 X）
    while True:
        keys = event.getKeys()
        if 'escape' in keys:
            print("⛔ ESC pressed before starting. Exiting...")
            win.close()
            core.quit()
            sys.exit(0)
        if keys:
            break
        if win.winHandle is None:
            print("❌ Window closed by user. Exiting...")
            win.close()
            core.quit()
            sys.exit(0)
        core.wait(0.05)


    # 3, 2, 1 , /...
    for countdown in range(3, 0, -1):
        text_stim.text = f'Starting in {countdown}...'
        text_stim.draw()
        win.flip()
        core.wait(1.0)

    results = []

    try:
        for i, trial in enumerate(trials):
            img_stim.image = os.path.join(cfg['image_folder'], trial['img'])
            trial_counter_stim.text = f"Trial {i + 1} / {len(trials)}"

            img_stim.draw()
            trial_counter_stim.draw()
            key_hint_stim.draw()
            win.flip()

            timer = core.Clock()
            if cfg['mode'] == 'fixed':
                keys = event.waitKeys(maxWait=cfg['fixed_duration'], keyList=list(cfg['response_keys'].keys()) + ['escape'], timeStamped=timer)
                core.wait(cfg['isi_duration'])
            else:
                keys = event.waitKeys(keyList=list(cfg['response_keys'].keys()) + ['escape'], timeStamped=timer)

            if keys:
                key, rt = keys[0]
                if key == 'escape':
                    print("⛔ Experiment manually terminated.")
                    break
                response = cfg['response_keys'][key]
                correct = int(response == trial['label'])
            else:
                response = 'F'
                rt = ''
                correct = 'F'

            results.append({
                'trial': i + 1,
                'image': trial['img'],
                'type': trial['type'],
                'expected': trial['label'],
                'response': response,
                'correct': correct,
            })

    finally:
        if results and not any(r['response'] == 'escape' for r in results):
            save_results(results, cfg['output_base'], subject_id, session_num, cfg)

        # 显示结束提示
        text_stim.text = "Experiment Completed!\n\nPress any key to continue..."
        text_stim.height = 0.08
        text_stim.draw()
        win.flip()
        event.waitKeys()  # ✅ 等待按键后再关闭窗口

        win.close()  # ✅ 只关闭当前窗口，保留主程序运行状态



