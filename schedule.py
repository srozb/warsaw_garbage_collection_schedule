from typing import (
    List,
    Union,
    Dict
)

import datetime
import requests

from pydantic import (
    BaseModel,
    validator
)

from config import config


class Fraction(BaseModel):
    data: datetime.datetime
    id_frakcja: str
    kod: str
    nazwa: str
    opis: str

    @validator('id_frakcja')
    def test_fraction_code(cls, v) -> bool:
        """Fraction code validator"""
        if v not in (config['fractions_to_monitor']):
            raise ValueError("Invalid code")
        return v


class Schedule(BaseModel):
    def fetch_schedule(self):
        data = f"_portalCKMjunkschedules_WAR_portalCKMjunkschedulesportlet_INSTANCE_o5AIb2mimbRJ_addressPointId={self.addressPointId}"
        return requests.post(self.url, data=data, params=self.param, headers=self.headers).json()[0]

    def update(self):
        self.raw_schedule = self.fetch_schedule()
        self.address = self.raw_schedule['adres']
        new_schedule = self.parse_schedules()
        if self.fraction == new_schedule:
            return
        self.fraction = new_schedule
        self.last_update = datetime.datetime.now()

    def parse_schedules(self):
        fraction = []
        for sch in self.raw_schedule['harmonogramy']:
            if sch['data'] == None:
                #print(f"No date for {sch['frakcja']['id_frakcja']}. Omitting.")
                continue
            for sub_sch in sch['frakcja']:
                sch[sub_sch] = sch['frakcja'][sub_sch]
            del sch['frakcja']
            sch['data'] = datetime.datetime.strptime(sch['data'], "%Y-%m-%d") + datetime.timedelta(hours=8)
            try:
                f = Fraction.parse_obj(sch)
                fraction.append(f)
            except ValueError:
                continue
        self.last_check = datetime.datetime.now()
        return fraction

    def as_msgs(self) -> List[Dict]:
        msgs = []
        for f in self.fraction:
            msgs.append({
                "topic": f"{config['mqtt']['topic']}/{f.id_frakcja}",
                "payload": f.json(),
                "qos": 0,
                "retain": True
                })
        return msgs

    addressPointId: int
    address: Union[str, None] = None
    last_check: Union[datetime.datetime, None] = None
    last_update: Union[datetime.datetime, None] = None
    url: str = "https://warszawa19115.pl/harmonogramy-wywozu-odpadow"
    param: Dict = {
        "p_p_id": "portalCKMjunkschedules_WAR_portalCKMjunkschedulesportlet_INSTANCE_o5AIb2mimbRJ",
        "p_p_lifecycle": 2,
        "p_p_state": "normal",
        "p_p_mode": "view",
        "p_p_resource_id": "ajaxResourceURL",
        "p_p_cacheability": "cacheLevelPage",
        "p_p_col_id": "column-1",
        "p_p_col_count": 1
    }
    headers: Dict = {'Content-Type': 'application/x-www-form-urlencoded'}
    fraction: Union[List[Fraction], None] = None
    raw_schedule: Dict = []
