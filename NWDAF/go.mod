module nwdaf.com

go 1.14

replace nwdaf.com/logger => ../logger

replace nwdaf.com/service => ../service

replace nwdaf.com/factory => ../factory

replace nwdaf.com/util => ../util

replace nwdaf.com/consumer => ../consumer

replace nwdaf.com/context => ../context

require (
	github.com/antonfisher/nested-logrus-formatter v1.3.0
	github.com/free5gc/logger_conf v1.0.0
	github.com/free5gc/logger_util v1.0.0
	github.com/free5gc/openapi v1.0.0
	github.com/free5gc/version v1.0.0
	github.com/google/uuid v1.3.0
	github.com/leodido/go-urn v1.2.1 // indirect
	github.com/sirupsen/logrus v1.7.0
	github.com/urfave/cli v1.22.4
	golang.org/x/sys v0.0.0-20201214210602-f9fddec55a1e // indirect
	gopkg.in/yaml.v2 v2.4.0
)
