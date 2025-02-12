{
    'name': 'The Real Estate',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'views/res_users_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
