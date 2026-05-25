FROM nginx:alpine

# Copy static frontend HTML
COPY index.html /usr/share/nginx/html/index.html

# Expose standard Nginx HTTP port
EXPOSE 80

# Substitute environment variable BACKEND_URL at container startup and start nginx.
# We limit envsubst to only replace '$BACKEND_URL' to prevent breaking other javascript variable structures.
CMD ["/bin/sh", "-c", "envsubst '$BACKEND_URL' < /usr/share/nginx/html/index.html > /usr/share/nginx/html/index.html.tmp && mv /usr/share/nginx/html/index.html.tmp /usr/share/nginx/html/index.html && exec nginx -g 'daemon off;'"]
