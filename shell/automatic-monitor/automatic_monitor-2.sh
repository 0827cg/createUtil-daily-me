#!/bin/bash

#Describe: Monitor Control System.
# tomcat, nginx, redis
#Author: cg
#Time: 2017-08-31

#----------USER CONFIG----------#

COMPUTER_NAME=105
TOMCAT_DIR=/home/xm6f/dev/tomcat-7.0.79
REDIS_DIR=/home/xm6f/dev/redis-3.2.4
REDIS_START_SHELL_CL=/home/xm6f/dev/shell/./redis_start_all.sh
#NGINX_DIR=/usr/local/nginx

TOMCAT_NUM=4

PORT_1=8080
PORT_2=8081
PORT_3=8088
PORT_4=8098

PORT_1_FILENAME=tomcat-8080
PORT_2_FILENAME=tomcat-8081
PORT_3_FILENAME=tomcat-8088
PORT_4_FILENAME=tomcat-8098

#REDIS_PORT=6379

#
GEN_FILE_TYPE=/dev/mapper/cl-root

EMAIL_LOG=/usr/scripts/automatic/monitor_log

EMAIL_ADDR_1=1542723438@qq.com
#EMAIL_ADDR_2=1679055895@qq.com

#-------------------------------#

TODAY_HMS=$(date +%y%m%d%H%M%S)
TODAY_H=$(date +%y%m%d%H)
YESTERDAY=$(date -d "yesterday" +%y%m%d)
TIME=$(date +%Y-%m-%d-%T)
HOUR=$(date +%H)
MIN=$(date +%M)


function createEmail_content() {
	if [[ $2 = -h ]]
	then
		if [[ $3 -eq 0 ]]
		then
			echo "$1" >> ${EMAIL_LOG}/email_content-${TODAY_H}.txt
		else
			echo -e "$1\c" >> ${EMAIL_LOG}/email_content-${TODAY_H}.txt
		fi
	else
		if [[ $3 -eq 0 ]]
		then
			echo "$1" >> ${EMAIL_LOG}/email_content-${TODAY_HMS}.txt
		else
			echo -e "$1\c" >> ${EMAIL_LOG}/email_content-${TODAY_HMS}.txt
		fi
	fi
}

function createEmail_errContent() {
        if [[ $2 = -h ]]
        then
                if [[ $3 -eq 0 ]]
                then
                        echo "$1" >> ${EMAIL_LOG}/email_err-${TODAY_H}.txt
                else
                        echo -e "$1\c" >> ${EMAIL_LOG}/email_err-${TODAY_H}.txt
                fi
        else
                if [[ $3 -eq 0 ]]
                then
                        echo "$1" >> ${EMAIL_LOG}/email_err-${TODAY_HMS}.txt
                else
                        echo -e "$1\c" >> ${EMAIL_LOG}/email_err-${TODAY_HMS}.txt
                fi
        fi
}


function startTomcat() {
	${1}/bin/./catalina.sh start
	if [[ $? -eq 0 ]]
	then
		createEmail_content "**-->脚本已对tomcat${2}执行启动命令"
	else
		createEmail_content "**-->脚本未成功对tomcat${2}执行命令"
	fi
	START_TOM_RESULT=$(ps -ef | grep tomcat)
	if [[ $START_TOM_RESULT =~ "$2" ]]
	then
		createEmail_content "**-->tomcat${2}已成功启动"
	else
		createEmail_content "**-->tomcat${2}启动未成功，请手动启动"
	fi	
}

function startRedis() {
	${REDIS_DIR}/./redis-server redis.conf
	if [[ $? -eq 0 ]]
	then
		createEmail_content "**-->脚本已对redis执行启动命令"
	else
		createEmail_content "**-->脚本未成功对reids执行命令"
	fi
	START_RED_RESULT=$(ps -ef | grep redis)
	if [[ $START_RED_RESULT =~ "redis-server" ]]
	then
		createEmail_content "**-->redis已成功启动"
	else
		createEmail_content "**-->redis启动未成功，请手动启动"
	fi
}

function startRedis_byShell() {
	${REDIS_START_SHELL_CL}
	if [[ $? -eq 0 ]]
	then
                createEmail_content "**-->脚本已对redis执行启动命令"
        else
                createEmail_content "**-->脚本未成功对reids执行命令"
        fi
        START_RED_RESULT=$(ps -ef | grep redis)
        if [[ $START_RED_RESULT =~ "redis-server" ]]
        then
                createEmail_content "**-->redis已成功启动"
        else
                createEmail_content "**-->redis启动未成功，请手动启动"
        fi

	
}
		

function startNginx() {
	${NGINX_DIR}/sbin/./nginx
	if [[ $? -eq 0 ]]
	then
		createEmail_content "**-->脚本已对nginx执行启动命令"
	else
		createEmail_content "**-->脚本未成功对nginx执行命令"
	fi
	START_NGINX_RESULT=$(ps -ef | grep nginx)
	if [[ $START_NGINX_RESULT =~ "nginx:" ]]
	then
		createEmail_content "**-->nginx已成功启动"
	else
		createEmail_content "**-->nginx启动未成功，请手动启动"
	fi
}

function try_start() {
        createEmail_content "* ${1}未运行"
        createEmail_content "**-->脚本将尝试进行启动...."
        if [[ -x "$2" ]]
        then
                if [[ ${1} -eq "redis" ]]
                then
                      	startRedis_byShell
                else
                        startNginx
                fi
        else
                createEmail_content "**-->${1}路径不存在"
                createEmail_content "**-->脚本启动${1}失败"
        fi
}



function createAll_tail() {

createEmail_content "======================================" $1
createEmail_content "---林繁" $1
createEmail_content "---$TIME" $1

}


function tomcat_h() {

        if [[ $TOMCAT_STATUS =~ "$1" ]]
        then
           	createEmail_content "* tomcat${1}---已在运行" -h 1
                TOMCAT_LOG=$(tail -n 150 ${TOMCAT_DIR}/${2}/logs/catalina.out)
                if [[ $TOMCAT_LOG =~ "exception" ]]
                then
                        createEmail_content "---日志输出异常" -h
                        createEmail_errContent "===============${COMPUTER_NAME}-${1}-输出日志===============" -h
                        createEmail_errContent "$TOMCAT_LOG" -h
                else
                        createEmail_content "---日志输出正常" -h
                fi
        else
               	createEmail_content "* tomcat${1}---未运行" -h

        fi
}


function tomcat_hms() {

	if [[ $TOMCAT_STATUS =~ "$1" ]]
	then
		TOMCAT_LOG=$(tail -n 150 ${TOMCAT_DIR}/${2}/logs/catalina.out)
		if [[ $TOMCAT_1_LOG =~ "exception" ]]
		then
			createEmail_content "* tomcat${1}---已运行---但日志输出异常"
			createEmail_errContent "===============${COMPUTER_NAME}-${1}-输出日志==============="
			createEmail_errContent "$TOMCAT_LOG"
		fi
	else
		createEmail_content "* tomcat${1}---未运行"
                createEmail_content "**-->脚本将尝试进行启动...."
                if [[ -x "${TOMCAT_DIR}/${2}" ]]
                then
                        startTomcat ${TOMCAT_DIR}/${2} ${1}
                else
                        createEmail_content "**-->tomcat${1}路径不存在"
                        createEmail_content "**-->脚本启动tomcat${1}失败"
                fi
	fi
}


function for_tomcat_h() {
	
	TOMCAT_STATUS=$(ps -ef | grep tomcat)
        for(( i=1; i<=${TOMCAT_NUM}; i++ )) {
                PORT=PORT_$i
		FILENAME=PORT_${i}_FILENAME
                eval TOMCAT_PORT="$"$PORT
		eval TOMCAT_FILENAME="$"$FILENAME
                tomcat_h $TOMCAT_PORT $TOMCAT_FILENAME
        }
}

function for_tomcat_hms() {

        TOMCAT_STATUS=$(ps -ef | grep tomcat)
        for(( i=1; i<=${TOMCAT_NUM}; i++ )) {
                PORT=PORT_$i
                FILENAME=PORT_${i}_FILENAME
                eval TOMCAT_PORT="$"$PORT
                eval TOMCAT_FILENAME="$"$FILENAME
                tomcat_hms $TOMCAT_PORT $TOMCAT_FILENAME
        }
}



function redis_state() {

        REDIS_STATUS=$(ps -ef | grep redis)
        if [[ $REDIS_STATUS =~ "redis-server" ]]
        then
                createEmail_content "* redis已在运行" -h
        else
                createEmail_content "* redis未运行" -h
        fi
}


function nginx_state() {

        NGINX_STATUS=$(ps -ef | grep nginx)
        if [[ $NGINX_STATUS =~ "nginx:" ]]
        then
                createEmail_content "* nginx已在运行" -h
        else
                createEmail_content "* nginx未运行" -h
        fi
}

function gen_state() {

        DISK_GEN_STATUS=$(df -h | grep $GEN_FILE_TYPE | awk '{print $5}' | cut -f 1 -d "%")
        if [[ $DISK_GEN_STATUS -lt 50 ]]
        then
                createEmail_content "* 根目录使用量较小---已使用${DISK_GEN_STATUS}%" -h
        else
                createEmail_content "* 根目录使用量较大---已使用${DISK_GEN_STATUS}%" -h
        fi
}


function redis_stats_hms() {

        REDIS_STATUS=$(ps -ef | grep redis)
        if [[ ! $REDIS_STATUS =~ "redis-server" ]]
	then
		try_start "redis" $REDIS_DIR
	fi
}

function nginx_stats_hms() {

        NGINX_STATUS=$(ps -ef | grep nginx)
        if [[ ! $NGINX_STATUS =~ "nginx:" ]]
	then
		try_start "nginx" $NGINX_DIR
	fi
}

function gen_stats_hms() {

        DISK_GEN_STATUS=$(df -h | grep $GEN_FILE_TYPE | awk '{print $5}' | cut -f 1 -d "%")
        if [[ $DISK_GEN_STATUS -gt 50 ]]
        then
                createEmail_content "* 根目录使用量较大---已使用${DISK_GEN_STATUS}%"
        fi
}

function rm_email_log() {

        rm ${EMAIL_LOG}/email_*-${YESTERDAY}*.txt
        if [[ $? -eq 0 ]]
        then
                createEmail_content "昨天的邮件日志已经删除" -h
        else
                createEmail_content "昨天的邮件日志未成功删除" -h
        fi
}


function automatic_h() {

        echo "" > ${EMAIL_LOG}/email_content-${TODAY_H}.txt

        createEmail_content "${COMPUTER_NAME}今日${HOUR}时脚本自动执行结果" -h
        createEmail_content "======================================" -h

        for_tomcat_h
        redis_state
        #nginx_state
        gen_state

	if [[ $HOUR = 23 ]]
	then
        	rm_email_log
	fi

        echo -e "\n\n" >> ${EMAIL_LOG}/email_content-${TODAY_H}.txt

        createAll_tail -h
}


function automatic_hms() {
	
	for_tomcat_hms
	redis_stats_hms
	#nginx_stats_hms
	gen_stats_hms
	
	if [[ -e "${EMAIL_LOG}/email_content-${TODAY_HMS}.txt" ]]
	then
		echo -e "\n\n" >> ${EMAIL_LOG}/email_content-${TODAY_HMS}.txt
		createAll_tail
	fi
}


#$HOUR_INT=$(echo $HOUR | sed -r 's/\<0+([1-9]+)/\1/g')

if [[ $MIN = 30 ]]
then
	automatic_h
	if [[ -e "${EMAIL_LOG}/email_err-${TODAY_H}.txt" ]]
	then
	      	mail -s "${COMPUTER_NAME}检测结果" -a ${EMAIL_LOG}/email_err-${TODAY_H}.txt $EMAIL_ADDR_1 < ${EMAIL_LOG}/email_content-${TODAY_H}.txt
	else
        	mail -s "${COMPUTER_NAME}检测结果" $EMAIL_ADDR_1 < ${EMAIL_LOG}/email_content-${TODAY_H}.txt
	fi
else
	automatic_hms
	if [[ -e "${EMAIL_LOG}/email_content-${TODAY_HMS}.txt" ]]
	then
		if [[ -e "${EMAIL_LOG}/email_err-${TODAY_HMS}.txt" ]]
		then
			mail -s "${COMPUTER_NAME}有服务未运行" -a ${EMAIL_LOG}/email_err-${TODAY_HMS}.txt $EMAIL_ADDR_1 < ${EMAIL_LOG}/email_content-${TODAY_HMS}.txt
		else
			mail -s "${COMPUTER_NAME}有服务未运行" $EMAIL_ADDR_1 < ${EMAIL_LOG}/email_content-${TODAY_HMS}.txt
		fi
	fi
fi


