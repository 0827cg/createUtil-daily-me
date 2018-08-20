SELECT
	htg_users.`name` AS studentName,
	htg_childcare_sign._studentid AS studentId,
	SUBSTR(CODE, 1, 8) AS codeNum,
	SUBSTR(CODE, 10, 22) AS appendTime,
	pic_url AS picUrl,
	org_id AS orgId,
	shop_id AS shopId
FROM
	htg_sign_pic
LEFT JOIN htg_childcare_sign ON htg_childcare_sign.id = htg_sign_pic.sign_ids
LEFT JOIN htg_users ON htg_users.id = htg_childcare_sign._studentid
WHERE
	shop_id IN (%d, %d)
ORDER BY
	htg_sign_pic.append_time DESC