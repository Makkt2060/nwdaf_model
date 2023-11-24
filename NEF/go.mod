module nef.com

go 1.14

replace nef.com/logger => ../logger

replace nef.com/service => ../service

replace nef.com/factory => ../factory

replace nef.com/util => ../util

replace nef.com/consumer => ../consumer

replace nef.com/context => ../context

require (
	github.com/antonfisher/nested-logrus-formatter v1.3.0
	github.com/free5gc/logger_conf v1.0.0
	github.com/free5gc/logger_util v1.0.0
	github.com/free5gc/openapi v1.0.0
	github.com/free5gc/version v1.0.0
	github.com/golang/groupcache v0.0.0-20200121045136-8c9f03a8e57e // indirect
	github.com/google/uuid v1.3.0
	github.com/leodido/go-urn v1.2.1 // indirect
	github.com/sirupsen/logrus v1.7.0
	github.com/urfave/cli v1.22.4
	golang.org/x/sys v0.0.0-20201214210602-f9fddec55a1e // indirect
	gopkg.in/yaml.v2 v2.4.0
)
