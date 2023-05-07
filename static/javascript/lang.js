
var Lang = {
    id: 'lpmx_lang_id',
    url0: "cfg/lang.csv",
    url1: "cfg/ldata.csv",
    left: 0,
    top: 0,
    wind: null,
    show: function () {
        if (!this.wind) return;
        this.wind.show();
    },
    hide: function () {
        if (!this.wind) return;
        this.wind.hide(this.id);
    },
    setXY: function () {
        this.wind.setXY(this.left, this.top, -1).show();
    },
    resetXY: function () {
        this.wind.reset();
        this.setXY();
    },
    read: async function () {

        const read_csv = async (url) => {
            const resp = await fetch(url, {
                method: 'GET',
                headers: { "Content-Type": "text/plain;charset=UTF-8" },
                cache: 'default'
            });
            if (resp.ok) {
                const csv_data = await resp.text();
                const rows = csv_data.trim().split("\n");
                return rows;
            }
            else {
                alert(`${url} Not Found.`);
                return [];
            }
        };
        const ls = await read_csv(this.url0);
        const ds = await read_csv(this.url1);
        const lmax = Math.max(ls.length, ds.length);
        const lds = [];
        for (let i = 0; i < lmax; i++) {
            lds.push(['', '']);
            if (i < ls.length)
                lds[i][0] = ls[i];
            if (i < ds.length)
                lds[i][1] = ds[i];
        }
        return lds;
    },
    open: async function () {
        let rows = await this.read();
        let rs = [];
        for (let row of rows) {
            let r = `<tr class="d"><td class="l">${row[0]}</td><td class="d">${row[1]}</td> </tr> `;
            rs.push(r);
        }
        const r = rs.join("");
        let html = `<table><tr class='h'><td>LANG</td><td>DATA</td></tr>${r}</table>
        `.replace(/\s+|\[rn]/g, ' ');

        if (!this.wind) {
            this.wind = UaWindowAdm.create(this.id, "lpmx_id");
            this.wind.linkToId("lpmx_pos_id", 10, 0, 0);
            this.wind.drag();
        }
        this.wind.setHtml(html);
        this.set_lang();
        this.show();
        const p = $("#" + this.id).offset();
        this.left = p.left;
        this.top = p.top;
    },
    set_lang: function () {
        $("#lpmx_lang_id").off("click");
        $("#lpmx_lang_id").on("click ", "table tr.d td.l", {}, function (e) {
            let L = $(this).html();
            FormLpmx.set_lang(L, "");
        });
        $("#lpmx_lang_id").on("click ", "table tr.d td.d", {}, function (e) {
            let D = $(this).html();
            FormLpmx.set_lang("", D);
        });
    }
};

