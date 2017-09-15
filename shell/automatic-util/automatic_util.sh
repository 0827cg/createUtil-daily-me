#!/bin/bash

#Describe: cut nginx log files and send email
#Author: cg
#Time: 2017-08-24

LOG_DIR=/usr/local/nginx/logs
TODAY=$(date +%y%m%d)
YESTERDAY=$(date -d "yesterday" +%y%m%d)
TIME=$(date +%Y-%m-%d-%T)
TOMCAT_DIR=/usr/local/tomcat

echo -e "\t149今日脚本自动执行结果" > email_content-$TODAY.txt
echo "======================================" >> email_content-$TODAY.txt

mv ${LOG_DIR}/access.log ${LOG_DIR}/access-${TODAY}.log
if [[ $? -eq 0 ]]
then
        kill -USR1 `cat ${LOG_DIR}/nginx.pid`
        if [[ $? -eq 0 ]]
        then
                echo "*nginx切割日志成功" >> email_content-$TODAY.txt
        else
                echo  "*nginx切割日志失败" >> email_content-$TODAY.txt
                echo "===============149-nginx-日志切割输出===============" >> email_err-$TODAY.txt
                kill -USR1 `cat ${LOG_DIR}/nginx.pid` 2>> email_err-$TODAY.txt
        fi
else
        echo  "*nginx切割日志失败" >> email_content-$TODAY.txt
        echo "===============149-nginx-日志拷贝输出===============" >> email_err-$TODAY.txt
        mv ${LOG_DIR}/access.log ${LOG_DIR}/access-${TODAY}.log 2>> email_err-$TODAY.txt
fi

ps_tomcat=$(ps -ef | grep tomcat)

if [[ $ps_tomcat =~ "8080" ]]
then
        echo -e "*tomcat8080---已在运行\c" >> email_content-$TODAY.txt
        tomcat8080_log=$(tail -n 150 ${TOMCAT_DIR}/lotmall-8080/logs/catalina.out)
        if [[ $tomcat8080_log =~ "exception" ]]
        then
                echo "---日志输出异常" >> email_content-$TODAY.txt
                echo "===============149-8080-输出日志===============" >> email_err-$TODAY.txt
                echo "$tomcat8080_log" >> email_err-$TODAY.txt
        else
                echo "---日志输出正常" >> email_content-$TODAY.txt
        fi
else
        echo "*tomcat8080---未运行" >> email_content-$TODAY.txt
fi

if [[ $ps_tomcat =~ '8081' ]]
then
        echo -e "*tomcat8081---已在运行\c" >> email_content-$TODAY.txt
        tomcat8081_log=$(tail -n 150 ${TOMCAT_DIR}/mango-8081/logs/catalina.out)
        if [[ $tomcat8081_log =~ "exception" ]]
        then
                echo "---日志输出异常" >> email_content-$TODAY.txt
                echo "===============149-8081-输出日志===============" >> email_err-$TODAY.txt
                echo "$tomcat8081_log" >> email_err-$TODAY.txt
        else
                echo "---日志输出正常" >> email_content-$TODAY.txt
        fi
else
        echo "*tomcat8081---未运行" >> email_content-$TODAY.txt
fi

if [[ $ps_tomcat =~ "8082" ]]
then
        echo -e "*tomcat8082---已在运行\c" >> email_content-$TODAY.txt
        tomcat8082_log=$(tail -n 150 ${TOMCAT_DIR}/tomcat-8082/logs/catalina.out)
        if [[ $tomcat8082_log =~ "exception" ]]
        then
                echo "---日志输出异常" >> email_content-$TODAY.txt
                echo "===============149-8082-输出日志===============" >> email_err-$TODAY.txt
                echo "$tomcat8082_log" >> email_err-$TODAY.txt
        else
                echo "---日志输出正常" >> email_content-$TODAY.txt
        fi
else
        echo "*tomcat8082---未运行" >> email_content-$TODAY.txt
fi

rm -rf email_content-$YESTERDAY.txt
if [[ $? -eq 0 ]]
then
        echo "*email_content-$YESTERDAY.txt已删除" >> email_content-$TODAY.txt
else
        echo "*email_content-$YESTERDAY.txt未删除，也许是不存在" >> email_content-$TODAY.txt
fi

if [[ -e "email_err-$YESTERDAY.txt"]]
then
	rm email_err-$YESTERDAY.txt
	echo "*email_err-$YESTERDAY.txt已删除" >> email_content-$TODAY.txt
else
fi


echo -e "\n\n" >> email_content-${TODAY}.txt
echo "======================================" >> email_content-${TODAY}.txt
echo "早点睡吧，兄弟" >> email_content-${TODAY}.txt
echo "晚安" >> email_content-${TODAY}.txt
echo "--${TIME}" >> email_content-${TODAY}.txt

if [[ -e "email_err-$TODAY.txt" ]]
then
        mail -s "149执行结果" -a email_err-$TODAY.txt 1542723438@qq.com < email_content-${TODAY}.txt
else
        mail -s "149执行结果" 1542723438@qq.com < email_content-${TODAY}.txt
fi

