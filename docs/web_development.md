# Web Development

Web development involves building websites and web applications. It encompasses frontend (client-side), backend (server-side), and everything in between.

## Frontend Development

The frontend is what users see and interact with in their browser. The three core technologies are:

- **HTML (HyperText Markup Language)**: Provides the structure and content of web pages using elements like headings, paragraphs, links, images, forms, and tables. HTML5 introduced semantic elements like `<header>`, `<nav>`, `<article>`, `<section>`, and `<footer>`.
- **CSS (Cascading Style Sheets)**: Controls the visual presentation — colors, fonts, layouts, animations. Modern CSS includes Flexbox and Grid for layout, media queries for responsive design, and CSS variables for theming.
- **JavaScript**: Adds interactivity and dynamic behavior. Handles DOM manipulation, event handling, API calls, and complex UI logic. Modern JavaScript (ES6+) includes arrow functions, template literals, destructuring, async/await, and modules.

Frontend frameworks like React, Vue.js, and Angular provide component-based architectures for building complex single-page applications (SPAs). SPAs load once and dynamically update content without full page reloads.

## Backend Development

The backend handles server-side logic, database interactions, authentication, and API endpoints. Common backend languages and frameworks include:

- **Python**: Flask (lightweight, minimal), Django (full-featured, batteries-included)
- **JavaScript/Node.js**: Express.js, Fastify
- **Java**: Spring Boot
- **Go**: Gin, Echo

Backend responsibilities include processing requests, querying databases, managing user sessions, handling file uploads, and implementing business logic.

## REST APIs

REST (Representational State Transfer) is an architectural style for designing web APIs. RESTful APIs use standard HTTP methods and follow these principles:

- Resources are identified by URLs (e.g., /api/users/123)
- HTTP methods map to CRUD operations: GET (read), POST (create), PUT/PATCH (update), DELETE (delete)
- Stateless — each request contains all information needed to process it
- Responses typically use JSON format

Status codes indicate the result: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Internal Server Error).

API versioning (e.g., /api/v1/users) allows backward-compatible changes. Rate limiting prevents abuse. Pagination handles large result sets.

## Authentication and Authorization

Authentication verifies who a user is. Common methods include:

- **Session-based**: Server stores session data, client holds a session cookie.
- **Token-based (JWT)**: Server issues a JSON Web Token containing user claims. The token is sent with each request in the Authorization header. JWTs are stateless and widely used in SPAs and mobile apps.
- **OAuth 2.0**: Delegated authorization protocol that allows third-party applications to access user data without sharing passwords.

Authorization determines what a user can do. Role-based access control (RBAC) assigns permissions based on user roles (admin, editor, viewer).

## Deployment and DevOps

Modern web deployment involves:

- **Containers (Docker)**: Package applications with their dependencies for consistent deployment across environments.
- **CI/CD**: Continuous Integration (automated testing on every commit) and Continuous Deployment (automated deployment to production).
- **Cloud platforms**: AWS, Google Cloud, Azure provide infrastructure for hosting, databases, storage, and more.
- **Reverse proxies**: Nginx and Apache handle SSL termination, load balancing, and static file serving in front of application servers.
- **CDNs (Content Delivery Networks)**: Cache and serve static assets from edge servers close to users, reducing latency.
