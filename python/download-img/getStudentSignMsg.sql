SELECT
	htg_users. NAME AS studentName,
	cacheTableTwo.studentId AS studentId,
	cacheTableTwo.orgId AS orgId,
	cacheTableTwo.shopId AS shopId,
	cacheTableTwo.codeNum AS codeNum,
	cacheTableTwo.picUrl AS picUrl,
	cacheTableTwo.appendTime AS appendTime
FROM
	(
		SELECT
			cacheTable.codeNum AS codeNum,
			cacheTable.appendTime AS appendTime,
			cacheTable.org_id AS orgId,
			cacheTable.shop_id AS shopId,
			cacheTable.sign_ids AS signIds,
			htg_childcare_sign._studentid AS studentId,
			cacheTable.pic_url AS picUrl
		FROM
			(
				SELECT
					SUBSTR(CODE, 1, 8) AS codeNum,
					SUBSTR(CODE, 10, 22) AS appendTime,
					pic_url,
					org_id,
					shop_id,
					sign_ids
				FROM
					htg_sign_pic
				WHERE
					org_id = %d
				AND shop_id IN (%d, %d)
			) cacheTable
		LEFT JOIN htg_childcare_sign ON htg_childcare_sign.id = cacheTable.sign_ids
	) cacheTableTwo
LEFT JOIN htg_users ON htg_users.id = cacheTableTwo.studentId