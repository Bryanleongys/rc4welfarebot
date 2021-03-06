import React from "react";
import { Container, Nav } from "react-bootstrap";
import { Switch, Route, Link, useRouteMatch } from "react-router-dom";
import GeneralFeedback from "./feedbacks/GeneralFeedback";
import EventFeedback from "./feedbacks/EventFeedback";

const FeedbackScreen = () => {
  let match = useRouteMatch();

  return (
    <Container>
      <Nav justify variant="tabs" defaultActiveKey="link-0">
        <Nav.Item>
          <Nav.Link as={Link} to={`${match.url}/general`} eventKey="link-0">
            General
          </Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link as={Link} to={`${match.url}/events`} eventKey="link-1">
            Events
          </Nav.Link>
        </Nav.Item>
      </Nav>
      <Switch>
        <Route path={`${match.url}/general`} component={GeneralFeedback} />
        <Route path={`${match.url}/events`} component={EventFeedback} />
      </Switch>
    </Container>
  );
};
export default FeedbackScreen;
