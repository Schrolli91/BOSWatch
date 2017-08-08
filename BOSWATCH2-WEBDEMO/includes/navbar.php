   <!-- Navigation -->
        <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index.html">BOSWatch Administration</a>
            </div>
            <!-- /.navbar-header -->

            <ul class="nav navbar-top-links navbar-right">

                <li class="dropdown">
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                        <i class="fa fa-bell fa-fw"></i> <i class="fa fa-caret-down"></i>
                    </a>
                    <ul class="dropdown-menu dropdown-alerts">
                        <li>
                            <a href="#">
                                <div>
                                    <i class="fa fa-comment fa-fw"></i> New Comment
                                    <span class="pull-right text-muted small">4 minutes ago</span>
                                </div>
                            </a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a href="#">
                                <div>
                                    <i class="fa fa-twitter fa-fw"></i> 3 New Followers
                                    <span class="pull-right text-muted small">12 minutes ago</span>
                                </div>
                            </a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a href="#">
                                <div>
                                    <i class="fa fa-envelope fa-fw"></i> Message Sent
                                    <span class="pull-right text-muted small">4 minutes ago</span>
                                </div>
                            </a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a href="#">
                                <div>
                                    <i class="fa fa-tasks fa-fw"></i> New Task
                                    <span class="pull-right text-muted small">4 minutes ago</span>
                                </div>
                            </a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a href="#">
                                <div>
                                    <i class="fa fa-upload fa-fw"></i> Server Rebooted
                                    <span class="pull-right text-muted small">4 minutes ago</span>
                                </div>
                            </a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a class="text-center" href="#">
                                <strong>See All Alerts</strong>
                                <i class="fa fa-angle-right"></i>
                            </a>
                        </li>
                    </ul>
                    <!-- /.dropdown-alerts -->
                </li>
                <!-- /.dropdown -->
                <li class="dropdown">
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                        <i class="fa fa-user fa-fw"></i> <i class="fa fa-caret-down"></i>
                    </a>
                    <ul class="dropdown-menu dropdown-user">
                        <li><a href="#"><i class="fa fa-user fa-fw"></i> User Profile</a>
                        </li>
                        <li><a href="#"><i class="fa fa-gear fa-fw"></i> Settings</a>
                        </li>
                        <li class="divider"></li>
                        <li><a href="login.html"><i class="fa fa-sign-out fa-fw"></i> Logout</a>
                        </li>
                    </ul>
                    <!-- /.dropdown-user -->
                </li>
                <!-- /.dropdown -->
            </ul>
            <!-- /.navbar-top-links -->

            <div class="navbar-default sidebar" role="navigation">
                <div class="sidebar-nav navbar-collapse">
                    <ul class="nav" id="side-menu">

                        <li>
                            <a href="index.php"><i class="fa fa-dashboard fa-fw"></i> Dashboard</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-bar-chart-o fa-fw"></i> Alarme<span class="fa arrow"></span></a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a href="a-overview.php">&Uuml;bersicht</a>
                                </li>
								<li>
                                    <a href="a-pocsag.php">POCSAG</a>
                                </li>
								<li>
                                    <a href="a-fms.php">FMS</a>
                                </li>
                                <li>
                                    <a href="a-zvei.php">ZVEI</a>
                                </li>
                            </ul>
                            <!-- /.nav-second-level -->
                        </li>
                       
                        <li>
                            <a href="#"><i class="fa fa-wrench fa-fw"></i> Einstellungen<span class="fa arrow"></span></a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a href="config.php">Globale Einstellungen</a>
                                </li>
                                 <li>
                                    <a href="#">Plugins <span class="fa arrow"></span></a>
                                    <ul class="nav nav-third-level">
                                        <li>
                                            <a href="#">BosMon</a>
                                        </li>
                                        <li>
                                            <a href="#">FFAgent</a>
                                        </li>
                                        <li>
                                            <a href="#">MySQL</a>
                                        </li>
                                        <li>
                                            <a href="#">Pushover</a>
                                        </li>
										<li>
                                            <a href="#">SMS</a>
                                        </li>
										<li>
                                            <a href="#">SMS77</a>
                                        </li>
										<li>
                                            <a href="#">Telegram</a>
                                        </li>
										<li>
                                            <a href="#">eMail</a>
                                        </li>
										<li>
                                            <a href="#">firEmergency</a>
                                        </li>
										<li>
                                            <a href="#">httpRequest</a>
                                        </li>
										<li>
                                            <a href="#">jsonSocket</a>
                                        </li>
										<li>
                                            <a href="#">notifyMyAndroid</a>
                                        </li>
										<li>
                                            <a href="#">yowsup</a>
                                        </li>
										<li>
                                            <a href="#">template</a>
                                        </li>
                                    </ul>
                                    <!-- /.nav-third-level -->
                                </li>
								<li>
                                    <a href="#">Addons <span class="fa arrow"></span></a>
                                    <ul class="nav nav-third-level">
                                        <li>
                                            <a href="#">AlarmMonitor Web</a>
                                        </li>
										<li>
                                            <a href="#">AlarmMonitor RPi</a>
                                        </li>
										<li>
                                            <a href="#">jsonSocketServer</a>
                                        </li>
										
                                        
                                    </ul>
                                    <!-- /.nav-third-level -->
                                </li>
								
								
                            </ul>
                            <!-- /.nav-second-level -->
                        </li>
						
						<li>
                            <a href="tester.php"><i class="fa fa-dashboard fa-fw"></i> Testcenter</a>
                        </li>
						
						
                       
                    </ul>
                </div>
                <!-- /.sidebar-collapse -->
            </div>
            <!-- /.navbar-static-side -->
        </nav>