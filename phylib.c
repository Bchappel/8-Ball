#include "phylib.h"

/*Constructors*/
phylib_object * phylib_new_still_ball(unsigned char number, phylib_coord * pos){

    phylib_object * new_ball = (phylib_object *)malloc(sizeof(phylib_object)); /*allocates memory for a new phylib_object*/

    if(new_ball == NULL){
        return NULL; /*if malloc fails, it will return NULL*/
    }

    new_ball->type = PHYLIB_STILL_BALL; /*sets the type to 'PHYLIB_STILL_BALL' */

    new_ball->obj.still_ball.number = number;
    new_ball->obj.still_ball.pos = *pos; /*transfers the information in the function parameters into the structure*/

    return new_ball; /*returns a pointer to the phylib_object*/

}

phylib_object * phylib_new_rolling_ball(unsigned char number, phylib_coord * pos, phylib_coord * vel, phylib_coord * acc){

    phylib_object * new_rolling_ball = (phylib_object *)malloc(sizeof(phylib_object)); /*allocates memory for a new rolling ball*/

    if(new_rolling_ball == NULL){
        return NULL; /*if malloc fails, it will return NULL*/
    }

    new_rolling_ball->type = PHYLIB_ROLLING_BALL; /*sets the type*/

    new_rolling_ball->obj.rolling_ball.number = number; /*number of the ball*/
    new_rolling_ball->obj.rolling_ball.pos = * pos; /*position*/
    new_rolling_ball->obj.rolling_ball.vel = * vel; /*ball velocity*/
    new_rolling_ball->obj.rolling_ball.acc = * acc; /*ball acc*/

    return new_rolling_ball;
}

phylib_object * phylib_new_hole(phylib_coord * pos){

    phylib_object * new_hole = (phylib_object *)malloc(sizeof(phylib_object)); /*allocates memory for a new hole*/

    if(new_hole == NULL){
        return NULL; /*if malloc fails, it will return NULL*/
    }

    new_hole->type = PHYLIB_HOLE; /*sets the type to phylib_hole*/
    new_hole->obj.hole.pos = *pos; /*sets the position of the hole*/
    return new_hole; /*return pointer to the new hole*/
}

phylib_object * phylib_new_hcushion(double y){

    phylib_object * new_hcushion = (phylib_object *)malloc(sizeof(phylib_object));

    if(new_hcushion == NULL){
        return NULL; /*if malloc fails, it will return NULL*/
    }    

    new_hcushion->type = PHYLIB_HCUSHION; /*sets the type to phylib_hcushion*/
    new_hcushion->obj.hcushion.y = y; /*sets the y coordinate of the cushion*/
    return new_hcushion; /*returns a pointer to the new cushion*/
}

phylib_object * phylib_new_vcushion(double x){

    phylib_object * new_vcushion = (phylib_object *)malloc(sizeof(phylib_object)); /*allocates memory for a new cushion*/

    if(new_vcushion == NULL){
        return NULL; /*if malloc fails, it will return NULL*/
    }    

    new_vcushion->type = PHYLIB_VCUSHION; /*sets the type to phylib_vcushion*/
    new_vcushion->obj.vcushion.x = x; /*sets the x coordinate of the cushion*/
    return new_vcushion; /*returns a pointer to the new cushion*/
}

phylib_table * phylib_new_table(void){

    phylib_table * new_table = (phylib_table*)malloc(sizeof(phylib_table));

    if(new_table == NULL){
        return NULL; /*returns null if the allocation fails*/
    }

    new_table->time = 0.0; /*sets the time to 0.0*/

    /*Allocate new cushions with constructor*/
    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    phylib_coord hole_positions[6] = {{0.0, 0.0}, {0.0, PHYLIB_TABLE_WIDTH},{0.0, PHYLIB_TABLE_LENGTH},{PHYLIB_TABLE_WIDTH, 0.0},{PHYLIB_TABLE_LENGTH / 2.0, PHYLIB_TABLE_LENGTH / 2.0},{PHYLIB_TABLE_LENGTH / 2.0, PHYLIB_TABLE_LENGTH}};

    for (int i = 0; i < 6; i++) {
        new_table->object[4 + i] = phylib_new_hole(&hole_positions[i]); /*adds the holes to the new table*/
    }

    for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++){
        new_table->object[i] = NULL; /*sets the rest of spaces reserved for the balls to NULL*/
    }

    return new_table; /*returns the table object*/
}

/*Utility Functions*/
void phylib_copy_object(phylib_object ** dest, phylib_object ** src){
    
    if(*src == NULL){ 
        *dest = NULL; /*If src is NULL, then dest is assigned NULL*/
    }else{

        *dest = (phylib_object *)malloc(sizeof(phylib_object)); /*Allocates memory for new phylib object*/

        if(*dest == NULL){
            return; /*if memory allocation fails*/
        }
        memcpy(*dest, *src, sizeof(phylib_object)); /*uses memcpy to copy*/
    }
}

phylib_table * phylib_copy_table(phylib_table * table){

    phylib_table * new_table = (phylib_table *)malloc(sizeof(phylib_table)); /*Allocate memory for a new table*/

    if(new_table == NULL){
       return NULL; /*if there is an error allocating memory, exit*/
    }

    new_table->time = table->time; /*copy over the time to the new table*/

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        phylib_copy_object(&(new_table->object[i]), &(table->object[i])); /*uses the phylib_copy_object function to copy items to the new table*/
    }

    return new_table; /*returns the new table*/
}

void phylib_add_object(phylib_table * table, phylib_object * object){

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] == NULL){
            table->object[i] = object; /*sets the address of the null object to address of object*/
            return; /*return once a NULL object is found*/
        }
    }
}

void phylib_free_table(phylib_table * table){

    if(table == NULL){
        return; /*if table is NULL, return*/
    }
       
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        free(table->object[i]); /*free the object*/
        table->object[i] = NULL; /*sets the object to NULL*/
    }

    free(table); /*free the table*/
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2){
    phylib_coord result;
    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;
    return result;
}

double phylib_length(phylib_coord c){
    double result = sqrt(c.x * c.x + c.y * c.y);    
    return result;
}

double phylib_dot_product(phylib_coord a, phylib_coord b){
    double result = a.x * b.x + a.y * b.y;
    return result;
}

double phylib_distance(phylib_object * obj1, phylib_object * obj2){

    if(obj1->type != PHYLIB_ROLLING_BALL){
        return -1.0; /*if obj1 is not a rolling ball, then return -1.0*/
    }

    double distance;
    phylib_coord c1, c2;

    c1 = obj1->obj.rolling_ball.pos; /*load the center coordinate of the rolling ball into c1*/

    switch (obj2->type){
        case PHYLIB_STILL_BALL:
        case PHYLIB_ROLLING_BALL:
            c2 = obj2->obj.rolling_ball.pos;
            distance = phylib_length(phylib_sub(c1, c2)) - PHYLIB_BALL_DIAMETER;
            break;
        case PHYLIB_HOLE:
            c2 = obj2->obj.hole.pos;
            distance = phylib_length(phylib_sub(c1, c2)) - PHYLIB_HOLE_RADIUS;
            break;
        case PHYLIB_HCUSHION:
            distance = fabs(c1.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
            break;
        case PHYLIB_VCUSHION:
            distance = fabs(c1.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
            break;
        default:
            return -1.0;
    }

    return fmax(0.0, distance); /*fmax to ensure the returned value is positive*/
}

/*Simulations*/
void phylib_roll(phylib_object * new, phylib_object * old, double time){

    if(new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL){
        return; /*if new or old are not rolling balls, return and do nothing*/
    }

    phylib_coord pos_old = old->obj.rolling_ball.pos; /*old position*/
    phylib_coord vel_old = old->obj.rolling_ball.vel; /*old velocity*/
    phylib_coord acc_old = old->obj.rolling_ball.acc; /*old acceleration*/

    /*Second integral of acceleration*/
    new->obj.rolling_ball.pos.x = pos_old.x + vel_old.x * time + 0.5 * acc_old.x * time * time;
    new->obj.rolling_ball.pos.y = pos_old.y + vel_old.y * time + 0.5 * acc_old.y * time * time;

    /*velocity of the new ball*/
    new->obj.rolling_ball.vel.x = vel_old.x + acc_old.x * time;
    new->obj.rolling_ball.vel.y = vel_old.y + acc_old.y * time;

    /*sets both the velocity and the acceleration to zero if sign changes*/
    if((vel_old.x * new->obj.rolling_ball.vel.x) < 0){
        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
    }

    /*sets both the velocity and the acceleration to zero if sign changes*/
    if((vel_old.y * new->obj.rolling_ball.vel.y) <= 0){
        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
    }
}

unsigned char phylib_stopped(phylib_object * object){

    double speed;
    phylib_coord vel = object->obj.rolling_ball.vel; /*gets the velocity from */
    speed = phylib_length(vel); /*calls the phylib length function*/

    if(speed < PHYLIB_VEL_EPSILON){
        object->type = PHYLIB_STILL_BALL; /*sets the type to still ball*/
        return 1; /*returns 1 if ball is converted*/
    }

    return 0; /*returns 0 if case fails*/
}

void phylib_bounce(phylib_object ** a, phylib_object ** b){

    phylib_coord r_ab;
    phylib_coord v_rel;
    phylib_coord n;
    double len_r_ab = 0;
    double v_rel_n = 0;

    phylib_coord pos_old = (*b)->obj.still_ball.pos; /*position*/
    phylib_coord vel_old = {0.0, 0.0}; /*sets the intial velocity of the still ball*/
    phylib_coord acc_old = {0,0}; /*sets the intial acceleration of the still ball*/

    switch((*b)->type){
        case PHYLIB_HCUSHION:
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * -1; /*y-velocity is negated*/
            (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * -1; /*y-acceleration is negated*/
            break;
        case PHYLIB_VCUSHION: 
            (*a)->obj.rolling_ball.vel.x *= -1; /*x-velocity is negated*/
            (*a)->obj.rolling_ball.acc.x *= -1; /*x-acceleration is negated*/
            break;
        case PHYLIB_HOLE:
            free(*a);
            (*a) = NULL;
            break;
        case PHYLIB_STILL_BALL:
            (*b)->type = PHYLIB_ROLLING_BALL; /*upgrade the still ball to a rolling ball*/
            (*b)->obj.rolling_ball.pos = pos_old; // Set initial position
            (*b)->obj.rolling_ball.vel = vel_old; // Set initial velocity
            (*b)->obj.rolling_ball.acc = acc_old; // Set initial acceleration

        case PHYLIB_ROLLING_BALL:
            /*compute the position of a with respect to b: subtract the position of b from a and call it r_ab*/
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

            /*compute the relative velocity of a with respect to b: subtract the velocity of b from a call it v_rel */
            v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

            /*divide the x and y components of r_ab by the length of r_ab; call that a normal vector, n*/
            len_r_ab = phylib_length(r_ab);
            n.x = r_ab.x / len_r_ab;
            n.y = r_ab.y / len_r_ab;

            /*calculate the ratio of the relative velocity, v_rel, in the direction of ball a by computing the dot_product of v_rel with respect to n: call that v_rel_n*/
            v_rel_n = phylib_dot_product(v_rel, n);

            /* Update the x and y velocities of ball a by subtracting the product of v_rel_n and vector n */
            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

            /* Update the x and y velocities of ball b by adding the product of v_rel_n and vector n */
            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

            /* Compute the speed of a and b as the lengths of their velocities. */
            double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

            /* Check if the speed is greater than PHYLIB_VEL_EPSILON. */
            if (speed_a > PHYLIB_VEL_EPSILON) {
                /* Set the acceleration of ball a to the negative velocity divided by the speed multiplied by PHYLIB_DRAG. */
                (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x / speed_a * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y / speed_a * PHYLIB_DRAG;
            }

            if (speed_b > PHYLIB_VEL_EPSILON) {
                /* Set the acceleration of ball b to the negative velocity divided by the speed multiplied by PHYLIB_DRAG. */
                (*b)->obj.rolling_ball.acc.x = -(*b)->obj.rolling_ball.vel.x / speed_b * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -(*b)->obj.rolling_ball.vel.y / speed_b * PHYLIB_DRAG;
            }
            break;
    }
}

unsigned char phylib_rolling(phylib_table * t){

    unsigned char count = 0;
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL){
            count++; /*increments the count as long as the object is not NULL*/
        }
    }

    return count;
}

phylib_table * phylib_segment(phylib_table * table){
    
    if(phylib_rolling(table) == 0){
        return NULL; /*if there are no rolling balls, return NULL*/
    }

    phylib_table * copy = phylib_copy_table(table); /*create a copy of the table*/

    if(copy == NULL){
        return NULL; /*if the copy fails, return NULL*/
    }

    double time = PHYLIB_SIM_RATE; /*time variable*/
    
    /*loop over time*/
    while(time < PHYLIB_MAX_TIME){

        /*loop over balls*/
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if (copy->object[i] != NULL && copy->object[i]->type == PHYLIB_ROLLING_BALL){
                phylib_roll(copy->object[i], table->object[i], time); /*apply the roll*/
                if (phylib_stopped(copy->object[i]) == 1){
                    copy->time += time; /*increment time*/
                    return copy; /*return the table*/
                }
            }
        }

        /*loop over balls*/
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if (copy->object[i] != NULL && copy->object[i]->type == PHYLIB_ROLLING_BALL){
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
                    if (i != j && copy->object[j] != NULL && phylib_distance(copy->object[i], copy->object[j]) <= 0.0){
                        phylib_bounce(&copy->object[i], &copy->object[j]); /*apply the bounce on a collision*/
                        copy->time += time; /*increment the time*/
                        return copy; /*return the table*/
                    }
                }
            }
        }
        time += PHYLIB_SIM_RATE; /*increment time*/
    }

    return copy; /*return the table*/
}

char * phylib_object_string(phylib_object * object){

    static char string[80];

    if(object == NULL){
        snprintf(string, 80, "NULL;");
        return string;
    }

    switch(object->type){

        case PHYLIB_STILL_BALL:
            snprintf(string, 80, "STILL_BALL (%d,%6.1lf,%6.1lf)", object->obj.still_ball.number, object->obj.still_ball.pos.x, object->obj.still_ball.pos.y);
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf(string, 80, "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)", object->obj.rolling_ball.number, object->obj.rolling_ball.pos.x, object->obj.rolling_ball.pos.y, object->obj.rolling_ball.vel.x, object->obj.rolling_ball.vel.y, object->obj.rolling_ball.acc.x, object->obj.rolling_ball.acc.y);
            break;
        case PHYLIB_HOLE:
            snprintf(string, 80, "HOLE (%6.1lf,%6.1lf)", object->obj.hole.pos.x, object->obj.hole.pos.y);
            break;
        case PHYLIB_HCUSHION:
            snprintf(string, 80, "HCUSHION (%6.1lf)", object->obj.hcushion.y);
            break;
        case PHYLIB_VCUSHION:
            snprintf(string, 80, "VCUSHION (%6.1lf)", object->obj.vcushion.x);
            break;
        }

    return string;
}
