# elasticsearch mapping

mapping = {
    u'company' : {
        'type' : 'multi_field',
        'fields' : {
            'name'  : { u'index': u'analyzed', u'store': u'yes', u'type': u'string', u'analyzer': u'eulang'       },
            'facet' : { u'index': u'analyzed', u'store': u'no',  u'type': u'string', u'analyzer': u'eulang_facet' },
        }
    },

    u'title'          : { u'index': u'analyzed', u'store': u'yes', u'type': u'string', u'analyzer': u'eulang', '_boost' : 1.2 },
    u'summary'        : { u'index': u'analyzed', u'store': u'yes', u'type': u'string', u'analyzer': u'eulang', '_boost' : 1.1 },
    u'category'       : { u'index': u'analyzed', u'store': u'yes', u'type': u'string', u'analyzer': u'eulang'   },
    u'content'        : { u'index': u'analyzed', u'store': u'yes', u'type': u'string', u'analyzer': u'eulang' },
    u'city'           : { u'index': u'analyzed', u'store': u'yes', u'type': u'string', u'analyzer': u'eulang' },

    u'published_date' : { u'type': u'date', u'format': u'YYYY-MM-dd HH:mm:ss' },
    u'details_url'    : { u'index': u'no', u'store': u'yes', u'type':  u'string' },
    u'image'          : { u'index': u'no', u'store': u'yes', u'type':  u'string' },

    u'source'         : { u'index': u'no', u'store': u'yes', u'type':  u'string' },
    u'source_label'   : { u'index': u'no', u'store': u'yes', u'type':  u'string' },

    u'pin' : {
        "properties" : {
            "location" : {
                "type" : "geo_point"
            }
        }
     }
}
