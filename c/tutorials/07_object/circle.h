#ifndef MYOBJ_H_INCLUDED
#define MYOBJ_H_INCLUDED

struct Circle{
    void (*new)(struct Circle*, float);
    float (*area)(struct Circle*);
    float radius; // todo: make it as private member field
    void (*setRadius)(struct Circle*, float);
    float (*getRadius)(struct Circle*);
};
typedef struct Circle Circle_t;

void newCircle(struct Circle *obj, float r);

#endif
