from pyhanlp import HanLP

document = """
新春伊始，衢州这家新材料企业的二期厂房正加紧建设。得益于当地在资金、人才引进等方面的支持，企业初创仅两年，研发就迈上新台阶，产值破亿元。

让企业专心发展，2023年，衢州市先后建成浙大衢州研究院等创新平台15个，成立博士创新站188家，实现创新平台对智能装备、新材料等六大产业链的全覆盖，为300余家企业解决相关技术难题500余项。

同时，衢州积极打造多样化的资金链服务体系，解决企业的资金需求，并成立企业综合服务中心，深入梳理解决产业链发展相关问题，进一步促进创新链、产业链、资金链、人才链深度融合。

今年以来，衢州市已完成亿元以上项目签约79个，总投资超924亿元，产业高质量发展不断提速。
"""
# 自动摘要
print(HanLP.extractSummary(document, 5))

