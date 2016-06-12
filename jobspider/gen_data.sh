
source /etc/profile


python $Jobspider/spider.py 

sleep 1

python $Jobspider/send_data/send_daily_data.py


