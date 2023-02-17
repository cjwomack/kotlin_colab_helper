#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// https://rosettacode.org/wiki/Input_loop#C
char *get_line(FILE* fp) {
    int len = 0, got = 0, c;
    char *buf = 0;

    while ((c = fgetc(fp)) != EOF) {
        if (got + 1 >= len) {
	len *= 2;
	if (len < 4) len = 4;
	    buf = realloc(buf, len);
	}
	buf[got++] = c;
	if (c == '\n') break;
    }
    if (c == EOF && !got) return 0;

    buf[got++] = '\0';
    return buf;
}

int main() {
    char *s;
    int count = 0;
    s = get_line(stdin);
    char fndir[50] = "/content/";
    char fn[50] = "";
    strcat(fn, &s[3]);
    int len = strlen(fn);
    fn[len - 1] = 0;
    strcat(fndir, fn);
    char fnkt[150];
    strcat(fnkt, ".kt");
    FILE *fptr;
    fptr = fopen(fnkt,"w");
    free(s);
    while ((s = get_line(stdin))) {
        fprintf(fptr,"%s",s);
        free(s);
    }
    fclose(fptr);

    FILE *fp;
    char path[500] = "/content/kotlinc/bin/kotlinc ";
    strcat(path, fn);
    strcat(path, ".kt -include-runtime -d /content/");
    strcat(path, fn);
    strcat(path, ".jar; java -jar /content/");
    strcat(path, fn);
    strcat(path, ".jar");
  

// https://stackoverflow.com/a/646254
  /* Open the command for reading. */
  
    fp = popen(path, "r");
    if (fp == NULL) {
        printf("Failed to run command\n" );
        exit(1);
    }

    /* Read the output a line at a time - output it. */
    char text[100];
  
    while (fgets(text, sizeof(text), fp) != NULL) {
        printf("%s", text);
    }

    /* close */
    pclose(fp);
    printf("\n");
  
    return 0;
}
