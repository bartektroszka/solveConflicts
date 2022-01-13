def check_success(merged, level, user):
    if level == 1:
        return merged

    if level == 2:
        if not merged:
            return False

        return True

    assert False


def init_level(level):
    if level < 0 or level > 2:
        return f"Podany zły poziom {level =}"

    session['level'] = level
    session.modified = True

    run_command(os.path.join('users_data', session['id']), f"./../../levels/level{level}/init_level.sh")

