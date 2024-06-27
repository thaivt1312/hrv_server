
// Importing files from Material-UI
import { useState } from "react";
import { AppBar, Toolbar, Typography, Button, useMediaQuery, styled, List, ListItemButton, ListItemText, Collapse } from "@mui/material"

import {ExpandMoreOutlined, ExpandLessOutlined, Menu as MenuIcon} from "@mui/icons-material"

// import MenuIcon from "@mui/icons-material/Menu";

// import ExpandLess from "@mui/icons-material/ExpandLess";
// import ExpandMore from "@mui/icons-material/ExpandMore";

// Using Inline Styling
const useStyles = styled((theme) => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
}));

// Exporting Default Navbar to the App.js File
export default function Navbar() {
    // const classes = useStyles();
    const small = useMediaQuery("(max-width:600px)");
    const full = useMediaQuery("(min-width:600px)");

    const [open, setOpen] = useState(false);

    const handleClick = () => {
        setOpen(!open);
    };

    return (
        <div style={{height: '10vh'}}>
            <AppBar position="static">
                <Toolbar variant="dense">
                    {small && (
                        <List>
                            <ListItemButton >
                                <Button
                                    onClick={
                                        handleClick
                                    }
                                >
                                    <MenuIcon />
                                    {open ? (
                                        <ExpandLessOutlined />
                                    ) : (
                                        <ExpandMoreOutlined />
                                    )}
                                </Button>
                                <Typography
                                    variant="h6"
                                    color="inherit"
                                    onClick={() => {
                                        console.log(
                                            "logo clicked"
                                        );
                                        setOpen(false);
                                    }}
                                >
                                    Smartwatch sound prediction system
                                </Typography>
                            </ListItemButton>
                            <Collapse
                                in={open}
                                timeout="auto"
                                unmountOnExit
                            >
                                <List
                                    component="div"
                                    disablePadding
                                >
                                    <ListItemButton >
                                        <ListItemText primary="Home" />
                                    </ListItemButton>
                                    <ListItemButton >
                                        <ListItemText primary="About" />
                                    </ListItemButton>{" "}
                                    <ListItemButton >
                                        <ListItemText primary="Contact" />
                                    </ListItemButton>
                                </List>
                            </Collapse>
                        </List>
                    )}

                    {full && (
                        <>
                            <Typography
                                variant="h6"
                                color="inherit"
                            >
                                Smartwatch sound prediction system
                            </Typography>
                            <Button color="inherit">
                                Home
                            </Button>

                            <Button color="inherit">
                                About
                            </Button>
                            <Button color="inherit">
                                Contact
                            </Button>
                        </>
                    )}
                </Toolbar>
            </AppBar>
        </div>
    );
}