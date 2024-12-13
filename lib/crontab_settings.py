from crontab import CronTab
from typing import Optional
from pydantic import BaseModel

web_cron = {
    'monday_active': True,
    'monday_on': '11:00',
    'monday_off': '19:00',
    'tuesday_active': True,
    'tuesday_on': '10:00',
    'tuesday_off': '18:00',
    'wednesday_active': True,
    'wednesday_on': '10:00',
    'wednesday_off': '16:00',
    'thursday_active': True,
    'thursday_on': '10:00',
    'thursday_off': '17:00',
    'friday_active': False,
    'friday_on': '00:00',
    'friday_off': '24:00',
    'saturday_active': False,
    'saturday_on': '00:00',
    'saturday_off': '24:00',
    'sunday_active': False
}


class crontab_model(BaseModel):
    monday_active: Optional[bool] = False
    monday_on: Optional[str] = "08:00"
    monday_off: Optional[str] = "18:00"
    tuesday_active: Optional[bool] = False
    tuesday_on: Optional[str] = "08:00"
    tuesday_off: Optional[str] = "18:00"
    wednesday_active: Optional[bool] = False
    wednesday_on: Optional[str] = "08:00"
    wednesday_off: Optional[str] = "18:00"
    thursday_active: Optional[bool] = False
    thursday_on: Optional[str] = "08:00"
    thursday_off: Optional[str] = "18:00"
    friday_active: Optional[bool] = False
    friday_on: Optional[str] = "08:00"
    friday_off: Optional[str] = "18:00"
    saturday_active: Optional[bool] = False
    saturday_on: Optional[str] = "08:00"
    saturday_off: Optional[str] = "18:00"
    sunday_active: Optional[bool] = False
    sunday_on: Optional[str] = "08:00"
    sunday_off: Optional[str] = "18:00"


def write_crontab(cron_user:str, cron_dict:dict):
    cron = CronTab(user=cron_user)
    weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

    for dow in weekdays:
        active = False
        cron_command='/usr/bin/curl http://127.0.0.1:5000/api/adcp/PowerOn -o /dev/null'
        cron_comment='ADCP ON'
        if dow == 'MON' and cron_dict['monday_active']:
            hh = cron_dict['monday_on'].split(':')[0]
            mm = cron_dict['monday_on'].split(':')[1]
            active = True
        elif dow == 'TUE' and cron_dict['tuesday_active']:
            hh = cron_dict['tuesday_on'].split(':')[0]
            mm = cron_dict['tuesday_on'].split(':')[1]
            active = True
        elif dow == 'WED' and cron_dict['wednesday_active']:
            hh = cron_dict['wednesday_on'].split(':')[0]
            mm = cron_dict['wednesday_on'].split(':')[1]
            active = True
        elif dow == 'THU' and cron_dict['thursday_active']:
            hh = cron_dict['thursday_on'].split(':')[0]
            mm = cron_dict['thursday_on'].split(':')[1]
            active = True
        elif dow == 'FRI' and cron_dict['friday_active']:
            hh = cron_dict['friday_on'].split(':')[0]
            mm = cron_dict['friday_on'].split(':')[1]
            active = True
        elif dow == 'SAT' and cron_dict['saturday_active']:
            hh = cron_dict['saturday_on'].split(':')[0]
            mm = cron_dict['saturday_on'].split(':')[1]
            active = True
        elif dow == 'SUN' and cron_dict['sunday_active']:
            hh = cron_dict['sunday_on'].split(':')[0]
            mm = cron_dict['sunday_on'].split(':')[1]
            active = True
            
        if active:
            job = cron.new(command=cron_command, comment=cron_comment)
            job.dow.on(dow)
            job.hour.on(hh)
            job.minute.on(mm)
    
    for dow in weekdays:
        active = False
        cron_command='/usr/bin/curl http://127.0.0.1:5000/api/adcp/PowerOff -o /dev/null'
        cron_comment='ADCP OFF'
        if dow == 'MON' and cron_dict['monday_active']:
            hh = cron_dict['monday_off'].split(':')[0]
            mm = cron_dict['monday_off'].split(':')[1]
            active = True
        elif dow == 'TUE' and cron_dict['tuesday_active']:
            hh = cron_dict['tuesday_off'].split(':')[0]
            mm = cron_dict['tuesday_off'].split(':')[1]
            active = True
        elif dow == 'WED' and cron_dict['wednesday_active']:
            hh = cron_dict['wednesday_off'].split(':')[0]
            mm = cron_dict['wednesday_off'].split(':')[1]
            active = True
        elif dow == 'THU' and cron_dict['thursday_active']:
            hh = cron_dict['thursday_off'].split(':')[0]
            mm = cron_dict['thursday_off'].split(':')[1]
            active = True
        elif dow == 'FRI' and cron_dict['friday_active']:
            hh = cron_dict['friday_off'].split(':')[0]
            mm = cron_dict['friday_off'].split(':')[1]
            active = True
        elif dow == 'SAT' and cron_dict['saturday_active']:
            hh = cron_dict['saturday_off'].split(':')[0]
            mm = cron_dict['saturday_off'].split(':')[1]
            active = True
        elif dow == 'SUN' and cron_dict['sunday_active']:
            hh = cron_dict['sunday_off'].split(':')[0]
            mm = cron_dict['sunday_off'].split(':')[1]
            active = True
            
        if active:
            job = cron.new(command=cron_command, comment=cron_comment)
            job.dow.on(dow)
            job.hour.on(hh)
            job.minute.on(mm)

    cron.write()
                
        
def read_crontab(cron_user:str):
    cron = CronTab(user=cron_user)
    cron_dict = crontab_model()
    
    for job in cron.find_comment('ADCP ON'):
        if job.dow == 'MON':
            cron_dict.monday_active = True
            cron_dict.monday_on = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'TUE':
            cron_dict.tuesday_active = True
            cron_dict.tuesday_on = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'WED':
            cron_dict.wednesday_active = True
            cron_dict.wednesday_on = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'THU':
            cron_dict.thursday_active = True
            cron_dict.thursday_on = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'FRI':
            cron_dict.friday_active = True
            cron_dict.friday_on = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'SAT':
            cron_dict.saturday_active = True
            cron_dict.saturday_on = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'SUN':
            cron_dict.sunday_active = True
            cron_dict.sunday_on = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'

    for job in cron.find_comment('ADCP OFF'):
        if job.dow == 'MON':
            cron_dict.monday_active = True
            cron_dict.monday_off = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'TUE':
            cron_dict.tuesday_active = True
            cron_dict.tuesday_off = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'WED':
            cron_dict.wednesday_active = True
            cron_dict.wednesday_off = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'THU':
            cron_dict.thursday_active = True
            cron_dict.thursday_off = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'FRI':
            cron_dict.friday_active = True
            cron_dict.friday_off = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'SAT':
            cron_dict.saturday_active = True
            cron_dict.saturday_off = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'
        elif job.dow == 'SUN':
            cron_dict.sunday_active = True
            cron_dict.sunday_off = f'{int(str(job.hour)):02d}:{int(str(job.minute)):02d}'


    return dict(cron_dict)

def remove_crontab(cron_user:str):
    cron = CronTab(user=cron_user)
    
    for job in cron.find_comment('ADCP ON'):
        cron.remove(job)
    for job in cron.find_comment('ADCP OFF'):
        cron.remove(job)
    cron.write()
    
if __name__ == "__main__":
    print("Starting")
    # write_crontab(cron_user='peter', cron_dict=web_cron)
    # cron_dict = read_crontab('peter')
    # print(cron_dict)
    #remove_crontab(cron_user='peter')
    print("The End")