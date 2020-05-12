# !!! Only 3:ALWAYS_ON 4:0 always off are available

def schedule_rule(schedule):
    """
        (:ADD (SCHEDULE-DATA :N "07-17 weekdays" :T SCHEDULE-DATA :D "On weekdays 7-17, otherwise off" :QT FACTOR)
          (SCHEDULE-RULE :N "weekdays 7-17" :T SCHEDULE-RULE :D NIL :RESTRICTION #(1 1 1 1 1 0 0) :VALUE (7 0 17 0 1 0.0))   ;;(6 0 18 0 1 0.0))
          (SCHEDULE-RULE :N DEFAULT :T SCHEDULE-RULE :D NIL :VALUE 0 :INDEX 1)
        )

        (:ADD (SCHEDULE-DATA :N "08-17 every day" :T SCHEDULE-DATA :D "On every day 8-17, otherwise off" :QT FACTOR)
              (SCHEDULE-RULE :N DEFAULT :T SCHEDULE-RULE :D NIL :VALUE (8 0 17 0 1))
        )

    :param schedule: plan_type 1:weekdays only 2:every day 3:ALWAYS_ON 4:0 always off
                    start
                    end
    :return:
    """

    if schedule['plan_type'] == 1:
        time = str(schedule['start']) + '-' + str(schedule['end'])
        shd_p1 = ' (:ADD (SCHEDULE-DATA :N "' + time + ' weekdays" :T SCHEDULE-DATA :D "On weekdays ' + time + \
                 ', otherwise off" :QT FACTOR)'
        shd_p2 = '(SCHEDULE-RULE :N "weekdays ' + time + '" :T SCHEDULE-RULE :D NIL :RESTRICTION #(1 1 1 1 1 0 0) :VALUE (' + \
                 str(schedule['start']) + ' 0 ' + str(schedule['end']) + ' 0 1 0.0))'
        shd_p3 = '(SCHEDULE-RULE :N DEFAULT :T SCHEDULE-RULE :D NIL :VALUE 0 :INDEX 1)'
        shd_p4 = ')'
        shd_tot = shd_p1 + shd_p2 + shd_p3 + shd_p4
        shd_name = time + ' weekdays'

    elif schedule['plan_type'] == 2:
        time = str(schedule['start']) + '-' + str(schedule['end'])
        shd_p1 = '(:ADD (SCHEDULE-DATA :N "' + time + ' every day" :T SCHEDULE-DATA :D "On every day ' + time + \
                 ', otherwise off" :QT FACTOR)'
        shd_p2 = '(SCHEDULE-RULE :N DEFAULT :T SCHEDULE-RULE :D NIL :VALUE (' + str(schedule['start']) + ' 0 ' + str(
            schedule['end']) + ' 0 1))'
        shd_p3 = ')'
        shd_tot = shd_p1 + shd_p2 + shd_p3
        shd_name = time + ' every day'

    elif schedule['plan_type'] == 3:
        shd_tot = ''
        shd_name = 'ALWAYS_ON'

    else:
        shd_tot = ''
        shd_name = '0'

    return shd_tot, shd_name