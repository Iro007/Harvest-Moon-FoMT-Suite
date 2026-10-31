#ifndef HELD_ITEM_HH
#define HELD_ITEM_HH

#include "prelude.h"

#include "rucksack_item.hh"

struct HeldItem
{
    HeldItem();

    enum Kind
    {
        KIND_FOOD,
        KIND_ARTICLE,
        KIND_2,
        KIND_3,
        KIND_4,
        KIND_5,
    };

    union PACKED Inner
    {
        struct
        {
            u8 id;
            i8 stamina_bonus;
            i8 fatigue_bonus;
        } food;

        struct
        {
            u8 id;
        } article;

        struct
        {
            u8 id;
        } unk_k3;

        u16 unk_k5_02;
    };

    Kind kind : 3;
    bool wrapped : 1;
    STRUCT_PAD(0x01, 0x02);
    Inner inner;
};

EC bool func_0800F190(HeldItem const * self);
EC HeldItem::Kind func_0800F204(HeldItem const * self);
EC RucksackItem func_0800F294(HeldItem const * self);
EC void func_0800F390(HeldItem * self);
EC void func_0800F418(HeldItem * self, RucksackItem rucksack_item);

#endif // HELD_ITEM_HH
