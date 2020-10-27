DROP DATABASE equipments;
CREATE DATABASE equipments;
USE equipments;

CREATE TABLE `详情` (
    `类型` ENUM("设备", "材料") NOT NULL,
    `名称` VARCHAR(60) NOT NULL,
    `型号` VARCHAR(30),
    `序列号` VARCHAR(30),
    `合同号` VARCHAR(60),
    `到货时间` DATE,
    `经办人` VARCHAR(30),
    `状态` ENUM("在用", "待用", "被借", "待维修", "维修中"),
    `存放位置` VARCHAR(30),
    `合同文件` VARCHAR(500),
    `照片` VARCHAR(150),
    `位置照片` VARCHAR(150),
    `备注` VARCHAR(500),
    PRIMARY KEY (`名称`, `型号`, `序列号`)
);

CREATE VIEW `数量统计`(`类型`, `名称`, `型号`, `数量`) AS
SELECT `类型`, `名称`, `型号`, COUNT(*)
FROM `详情`
GROUP BY `类型`, `名称`, `型号`;

INSERT INTO `详情`(`类型`, `名称`, `型号`, `序列号`, `合同号`, `到货时间`, `经办人`, `状态`, `存放位置`, `合同文件`, `照片`, `位置照片`, `备注`)
VALUES('设备', '激光器', '1型', 'cx123', '11245134', '2018-02-03', '陈思源', '在用', '1号台', NULL, NULL, NULL, NULL);

INSERT INTO `详情`(`类型`, `名称`, `型号`, `序列号`, `合同号`, `到货时间`, `经办人`, `状态`, `存放位置`, `合同文件`, `照片`, `位置照片`, `备注`)
VALUES('材料', '探头', 'A型', 'pb234', '265463', '2018-09-11', '陈思源', '在用', '1号台', NULL, NULL, NULL, NULL);

